from .alert_event import AlertEvent
from .emergency_mediator import IEmergencyMediator
from .observers import IAlertObserver


class EmergencyBridgeObserver(IAlertObserver):
    def __init__(self, mediator: IEmergencyMediator):
        if mediator is None:
            raise ValueError("mediator must not be None")
        self._mediator = mediator

    def update(self, alert_event: AlertEvent) -> None:
        if alert_event.severity == "CRITICAL":
            self._mediator.handle_alert(alert_event)
