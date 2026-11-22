import contextlib
import io
import unittest
from datetime import datetime

from src.alert_event import AlertEvent
from src.emergency_bridge_observer import EmergencyBridgeObserver
from src.emergency_devices import (
    AlarmController,
    DoorController,
    VentilationController,
)
from src.emergency_mediator import EmergencyMediator, IEmergencyMediator


class EmergencyMediatorTests(unittest.TestCase):
    def setUp(self):
        self.alarm = AlarmController()
        self.door = DoorController()
        self.ventilation = VentilationController()
        self.mediator = EmergencyMediator(self.alarm, self.door, self.ventilation)

    def make_alert(self, severity):
        return AlertEvent("Lab", 75.0, "% smoke", severity, datetime.now())

    def test_critical_alert_coordinates_emergency_devices(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.mediator.handle_alert(self.make_alert("CRITICAL"))
        self.assertTrue(self.alarm.is_active)
        self.assertTrue(self.door.is_unlocked)
        self.assertTrue(self.ventilation.is_active)

    def test_warning_does_not_activate_emergency_devices(self):
        self.mediator.handle_alert(self.make_alert("WARNING"))
        self.assertFalse(self.alarm.is_active)
        self.assertFalse(self.door.is_unlocked)
        self.assertFalse(self.ventilation.is_active)

    def test_bridge_sends_critical_alert_to_mediator(self):
        self.assertIsInstance(self.mediator, IEmergencyMediator)
        bridge = EmergencyBridgeObserver(self.mediator)
        with contextlib.redirect_stdout(io.StringIO()):
            bridge.update(self.make_alert("CRITICAL"))
        self.assertTrue(self.alarm.is_active)
        self.assertTrue(self.door.is_unlocked)
        self.assertTrue(self.ventilation.is_active)

    def test_bridge_ignores_warning_alert(self):
        bridge = EmergencyBridgeObserver(self.mediator)
        bridge.update(self.make_alert("WARNING"))
        self.assertFalse(self.alarm.is_active)
        self.assertFalse(self.door.is_unlocked)
        self.assertFalse(self.ventilation.is_active)


if __name__ == "__main__":
    unittest.main()
