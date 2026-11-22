# Nguyễn Hải Đăng - MSSV: 202418863

from src.emergency_bridge_observer import EmergencyBridgeObserver
from src.emergency_devices import (
    AlarmController,
    DoorController,
    VentilationController,
)
from src.emergency_mediator import EmergencyMediator
from src.legacy_smoke_detector import LegacySmokeDetector
from src.observers import AuditLogObserver, DashboardObserver, EmailAlertObserver
from src.sensor_monitor import SensorMonitor
from src.smoke_sensor_adapter import SmokeSensorAdapter


def main() -> None:
    old_detector = LegacySmokeDetector(735)
    sensor = SmokeSensorAdapter(old_detector)
    monitor = SensorMonitor()
    alarm = AlarmController()
    door = DoorController()
    ventilation = VentilationController()
    mediator = EmergencyMediator(alarm, door, ventilation)
    audit_log = AuditLogObserver()
    monitor.attach(DashboardObserver())
    monitor.attach(EmailAlertObserver())
    monitor.attach(audit_log)
    monitor.attach(EmergencyBridgeObserver(mediator))

    print("--- Smoke level: WARNING ---")
    old_detector.set_smoke_level(600)
    monitor.check_sensor("Computer lab smoke", sensor)

    print("\n--- Smoke level: CRITICAL ---")
    old_detector.set_smoke_level(735)
    monitor.check_sensor("Computer lab smoke", sensor)


if __name__ == "__main__":
    main()
