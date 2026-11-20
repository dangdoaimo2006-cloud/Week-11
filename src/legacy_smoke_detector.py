class LegacySmokeDetector:
    def __init__(self, smoke_level: int):
        self._smoke_level = max(0, min(1000, smoke_level))

    def get_smoke_level(self) -> int:
        return self._smoke_level

    def get_description(self) -> str:
        return "Legacy smoke detector"

    def set_smoke_level(self, value: int) -> None:
        self._smoke_level = max(0, min(1000, value))
