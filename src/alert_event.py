from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AlertEvent:
    sensor_name: str
    value: float
    unit: str
    severity: str
    occurred_at: datetime
