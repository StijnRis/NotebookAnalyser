from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Generic, Sequence, TypeVar

from .event import Event



class EventLog(ABC):
    idle_threshold = timedelta(minutes=3)

    @abstractmethod
    def get_events(self) -> Sequence[Event]:
        """
        Returns the list of events.
        """
        pass

    def get_active_periods(self) -> list[tuple[datetime, datetime]]:
        event_sequence = self.get_events()

        active_periods: list[tuple[datetime, datetime]] = []
        start_time = None
        previous_time = None
        for event in event_sequence:
            event_time = event.get_time()

            if start_time is None or previous_time is None:
                start_time = event_time

            elif (event_time - previous_time) > self.idle_threshold:
                active_periods.append((start_time, previous_time))
                start_time = event_time

            previous_time = event_time

        if start_time is not None:
            active_periods.append((start_time, event_sequence[-1].get_time()))

        return active_periods
