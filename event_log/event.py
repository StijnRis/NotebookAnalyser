from abc import ABC
from abc import abstractmethod
from datetime import datetime


class Event(ABC):
    @abstractmethod
    def get_time(self) -> datetime:
        pass
