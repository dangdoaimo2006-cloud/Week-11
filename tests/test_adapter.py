import unittest

from src.legacy_smoke_detector import LegacySmokeDetector
from src.sensor import ISensor
from src.smoke_sensor_adapter import SmokeSensorAdapter


class SmokeSensorAdapterTests(unittest.TestCase):
    def test_adapter_returns_percent_and_unit(self):
        sensor = SmokeSensorAdapter(LegacySmokeDetector(735))
        self.assertIsInstance(sensor, ISensor)
        self.assertEqual(sensor.read_value(), 73.5)
        self.assertEqual(sensor.get_unit(), "% smoke")

    def test_adapter_reads_current_legacy_value(self):
        legacy = LegacySmokeDetector(100)
        sensor = SmokeSensorAdapter(legacy)
        legacy.set_smoke_level(640)
        self.assertEqual(sensor.read_value(), 64.0)

    def test_legacy_detector_clamps_its_input(self):
        self.assertEqual(LegacySmokeDetector(1500).get_smoke_level(), 1000)
        self.assertEqual(LegacySmokeDetector(-20).get_smoke_level(), 0)

    def test_adapter_rejects_missing_legacy_detector(self):
        with self.assertRaises(ValueError):
            SmokeSensorAdapter(None)


if __name__ == "__main__":
    unittest.main()
