import contextlib
import io
import unittest
from dataclasses import FrozenInstanceError

from src.alert_event import AlertEvent
from src.legacy_smoke_detector import LegacySmokeDetector
from src.observers import AuditLogObserver, IAlertObserver
from src.sensor_monitor import SensorMonitor
from src.smoke_sensor_adapter import SmokeSensorAdapter


class SavingObserver(IAlertObserver):
    def __init__(self, monitor=None, remove=None):
        self.events = []
        self.monitor = monitor
        self.remove = remove

    def update(self, alert_event):
        self.events.append(alert_event)
        if self.monitor is not None and self.remove is not None:
            self.monitor.detach(self.remove)


class BrokenObserver(IAlertObserver):
    def update(self, alert_event):
        raise RuntimeError("test observer failure")


class SensorMonitorTests(unittest.TestCase):
    def make_sensor(self, level):
        return SmokeSensorAdapter(LegacySmokeDetector(level))

    def test_thresholds_and_immutable_event(self):
        monitor = SensorMonitor()
        observer = SavingObserver()
        monitor.attach(observer)

        self.assertIsNone(monitor.check_sensor("lab", self.make_sensor(499)))
        warning = monitor.check_sensor("lab", self.make_sensor(500))
        critical = monitor.check_sensor("lab", self.make_sensor(700))

        self.assertEqual(warning.severity, "WARNING")
        self.assertEqual(critical.severity, "CRITICAL")
        self.assertEqual(len(observer.events), 2)
        with self.assertRaises(FrozenInstanceError):
            warning.value = 0

    def test_attach_does_not_register_same_observer_twice(self):
        monitor = SensorMonitor()
        observer = SavingObserver()
        monitor.attach(observer)
        monitor.attach(observer)
        monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(len(observer.events), 1)

    def test_detach_stops_future_alerts(self):
        monitor = SensorMonitor()
        observer = SavingObserver()
        monitor.attach(observer)
        monitor.detach(observer)
        monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(observer.events, [])

    def test_observer_can_detach_another_during_notification(self):
        monitor = SensorMonitor()
        later_observer = SavingObserver()
        first_observer = SavingObserver(monitor, later_observer)
        monitor.attach(first_observer)
        monitor.attach(later_observer)

        monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(len(later_observer.events), 1)
        monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(len(later_observer.events), 1)

    def test_broken_observer_does_not_stop_other_observers(self):
        monitor = SensorMonitor()
        observer = SavingObserver()
        monitor.attach(BrokenObserver())
        monitor.attach(observer)

        with contextlib.redirect_stderr(io.StringIO()):
            monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(len(observer.events), 1)

    def test_audit_observer_keeps_alert(self):
        monitor = SensorMonitor()
        audit = AuditLogObserver()
        monitor.attach(audit)
        with contextlib.redirect_stdout(io.StringIO()):
            monitor.check_sensor("lab", self.make_sensor(650))
        self.assertEqual(len(audit.events), 1)


if __name__ == "__main__":
    unittest.main()
