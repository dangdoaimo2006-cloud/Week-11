from abc import ABC, abstractmethod

from .alert_event import AlertEvent
from .emergency_devices import (
    AlarmController,
    DoorController,
    VentilationController,
)


class IEmergencyMediator(ABC):
    @abstractmethod
    def handle_alert(self, alert_event: AlertEvent) -> None:
        pass


class EmergencyMediator(IEmergencyMediator):
    def __init__(
        self,
        alarm: AlarmController,
        door: DoorController,
        ventilation: VentilationController,
    ):
        self._alarm = alarm
        self._door = door
        self._ventilation = ventilation

    def handle_alert(self, alert_event: AlertEvent) -> None:
        if alert_event.severity != "CRITICAL":
            return

        self._alarm.activate()
        self._door.unlock()
        self._ventilation.activate()
