class AlarmController:
    def __init__(self):
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
        print("[ALARM] Activated")


class DoorController:
    def __init__(self):
        self.is_unlocked = False

    def unlock(self) -> None:
        self.is_unlocked = True
        print("[DOOR] Emergency exit unlocked")


class VentilationController:
    def __init__(self):
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
        print("[VENTILATION] Activated")
