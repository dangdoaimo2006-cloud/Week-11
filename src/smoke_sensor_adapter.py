from .legacy_smoke_detector import LegacySmokeDetector
from .sensor import ISensor


class SmokeSensorAdapter(ISensor):
    def __init__(self, legacy_sensor: LegacySmokeDetector):
        if legacy_sensor is None:
            raise ValueError("legacy_sensor must not be None")
        self._legacy_sensor = legacy_sensor

    def read_value(self) -> float:
        return self._legacy_sensor.get_smoke_level() / 10.0

    def get_unit(self) -> str:
        return "% smoke"
