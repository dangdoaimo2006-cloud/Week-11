from abc import ABC, abstractmethod

from .alert_event import AlertEvent


class IAlertObserver(ABC):
    @abstractmethod
    def update(self, alert_event: AlertEvent) -> None:
        pass


class DashboardObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        print(
            f"[DASHBOARD] {alert_event.sensor_name}: "
            f"{alert_event.value:.1f}{alert_event.unit} "
            f"[{alert_event.severity}]"
        )


class EmailAlertObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        print(
            f"[EMAIL SIMULATED] {alert_event.severity}: "
            f"{alert_event.sensor_name} at "
            f"{alert_event.value:.1f}{alert_event.unit}"
        )


class AuditLogObserver(IAlertObserver):
    def __init__(self):
        self.events: list[AlertEvent] = []

    def update(self, alert_event: AlertEvent) -> None:
        self.events.append(alert_event)
        print(f"[AUDIT] Saved {alert_event.severity} alert")
