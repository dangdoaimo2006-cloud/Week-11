import logging
from datetime import datetime

from .alert_event import AlertEvent
from .observers import IAlertObserver
from .sensor import ISensor


class SensorMonitor:
    def __init__(self):
        self._observers: list[IAlertObserver] = []
        self._logger = logging.getLogger(__name__)

    def attach(self, observer: IAlertObserver) -> None:
        if observer is None:
            raise ValueError("observer must not be None")
        if not any(item is observer for item in self._observers):
            self._observers.append(observer)

    def detach(self, observer: IAlertObserver) -> None:
        self._observers = [item for item in self._observers if item is not observer]

    def check_sensor(self, sensor_name: str, sensor: ISensor) -> AlertEvent | None:
        value = sensor.read_value()
        if value >= 70:
            severity = "CRITICAL"
        elif value >= 50:
            severity = "WARNING"
        else:
            return None

        alert_event = AlertEvent(
            sensor_name=sensor_name,
            value=value,
            unit=sensor.get_unit(),
            severity=severity,
            occurred_at=datetime.now(),
        )
        self._notify(alert_event)
        return alert_event

    def _notify(self, alert_event: AlertEvent) -> None:
        for observer in self._observers.copy():
            try:
                observer.update(alert_event)
            except Exception:
                self._logger.exception("Alert observer failed: %r", observer)
