import contextlib
import io
import unittest

from src.emergency_bridge_observer import EmergencyBridgeObserver
from src.emergency_devices import (
    AlarmController,
    DoorController,
    VentilationController,
)
from src.emergency_mediator import EmergencyMediator
from src.legacy_smoke_detector import LegacySmokeDetector
from src.observers import AuditLogObserver
from src.sensor_monitor import SensorMonitor
from src.smoke_sensor_adapter import SmokeSensorAdapter


class CampusSafetyFlowTests(unittest.TestCase):
    def setUp(self):
        self.legacy = LegacySmokeDetector(0)
        self.sensor = SmokeSensorAdapter(self.legacy)
        self.monitor = SensorMonitor()
        self.alarm = AlarmController()
        self.door = DoorController()
        self.ventilation = VentilationController()
        self.mediator = EmergencyMediator(
            self.alarm, self.door, self.ventilation
        )
        self.audit = AuditLogObserver()
        self.monitor.attach(self.audit)
        self.monitor.attach(EmergencyBridgeObserver(self.mediator))

    def test_warning_is_recorded_without_emergency_response(self):
        self.legacy.set_smoke_level(600)
        with contextlib.redirect_stdout(io.StringIO()):
            alert = self.monitor.check_sensor("Room 1", self.sensor)

        self.assertEqual(alert.severity, "WARNING")
        self.assertEqual(len(self.audit.events), 1)
        self.assertFalse(self.alarm.is_active)
        self.assertFalse(self.door.is_unlocked)
        self.assertFalse(self.ventilation.is_active)

    def test_critical_alert_reaches_observer_and_mediator(self):
        self.legacy.set_smoke_level(735)
        with contextlib.redirect_stdout(io.StringIO()):
            alert = self.monitor.check_sensor("Room 1", self.sensor)

        self.assertEqual(alert.severity, "CRITICAL")
        self.assertIs(self.audit.events[0], alert)
        self.assertTrue(self.alarm.is_active)
        self.assertTrue(self.door.is_unlocked)
        self.assertTrue(self.ventilation.is_active)


if __name__ == "__main__":
    unittest.main()
