# Nguyễn Hải Đăng - MSSV: 202418863

from src.legacy_smoke_detector import LegacySmokeDetector
from src.observers import AuditLogObserver, DashboardObserver, EmailAlertObserver
from src.sensor_monitor import SensorMonitor
from src.smoke_sensor_adapter import SmokeSensorAdapter


def main() -> None:
    old_detector = LegacySmokeDetector(735)
    sensor = SmokeSensorAdapter(old_detector)
    monitor = SensorMonitor()
    audit_log = AuditLogObserver()
    monitor.attach(DashboardObserver())
    monitor.attach(EmailAlertObserver())
    monitor.attach(audit_log)

    print(f"{sensor.read_value():.1f} {sensor.get_unit()}")
    monitor.check_sensor("Computer lab smoke", sensor)


if __name__ == "__main__":
    main()
