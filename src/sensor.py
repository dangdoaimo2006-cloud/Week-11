from abc import ABC, abstractmethod


class ISensor(ABC):
    @abstractmethod
    def read_value(self) -> float:
        pass

    @abstractmethod
    def get_unit(self) -> str:
        pass
