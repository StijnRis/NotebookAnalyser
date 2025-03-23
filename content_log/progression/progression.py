from abc import ABC, abstractmethod


class Progression(ABC):
    @abstractmethod
    def get_times(self) -> list[float]:
        pass

    @abstractmethod
    def get_progression(self) -> list[float]:
        pass
