# Nguyễn Hải Đăng - MSSV: 202418863

from src.legacy_smoke_detector import LegacySmokeDetector
from src.smoke_sensor_adapter import SmokeSensorAdapter


def main() -> None:
    old_detector = LegacySmokeDetector(735)
    sensor = SmokeSensorAdapter(old_detector)

    print(f"{sensor.read_value():.1f} {sensor.get_unit()}")


if __name__ == "__main__":
    main()
