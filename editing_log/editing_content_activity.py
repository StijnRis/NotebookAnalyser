from datetime import timedelta
from typing import List, Optional

from editing_log.content_event import (
    ContentEvent,
    FileHiddenEvent,
    FileVisibleEvent,
)


class EditingContentActivity:
    """
    A collection of content events
    """

    def __init__(
        self,
        events: List[ContentEvent],
    ):
        self.events = events
        self.idle_threshold = timedelta(minutes=4)

        self.events.sort(key=lambda x: x.get_time())

        self.check_invariants()

    def check_invariants(self):
        # Check that the log entries are sorted by time
        for i in range(1, len(self.events)):
            assert (
                self.events[i].get_time() >= self.events[i - 1].get_time()
            ), "Log entries should be sorted by event time"

    def get_start_time(self):
        for entry in self.events:
            if not isinstance(entry, (FileVisibleEvent, FileHiddenEvent)):
                return entry.get_time()
        assert False, "No event found"

    def get_end_time(self):
        for entry in reversed(self.events):
            if not isinstance(entry, (FileVisibleEvent, FileHiddenEvent)):
                return entry.get_time()
        assert False, "No event found"

    def get_completion_time(self):
        """
        Get time between the first and last event
        """

        return self.get_end_time() - self.get_start_time()

    def get_file_open_time(self) -> timedelta:
        """
        Calculate the total time of having the file open
        """

        active_time = timedelta(0)
        last_time = None

        for event in self.events:
            event_time = event.get_time()

            if isinstance(event, FileVisibleEvent):
                last_time = None

            if last_time is not None:
                active_time += event_time - last_time

            last_time = event_time

        return active_time

    def get_file_usage_time(self) -> timedelta:
        """
        Calculate the total time of using the file
        """

        active_time = timedelta(0)
        last_edit_time = None

        for entry in self.events:
            event_time = entry.get_time()

            if last_edit_time is not None:
                time_between = event_time - last_edit_time
                if time_between <= self.idle_threshold:
                    active_time += time_between

            last_edit_time = event_time

        return active_time

    def get_amount_of_events(self):
        return len(self.events)

    def get_event_by_index(self, index: int) -> Optional[ContentEvent]:
        if 0 <= index < len(self.events):
            return self.events[index]
        return None

    def get_amount_of_tab_switches(self):
        total = 0
        for entry in self.events:
            if isinstance(entry, FileVisibleEvent):
                total += 1

        return total

    def get_event_sequence(self):
        """
        Returns a list of tuples with the event time and event name.
        """

        return [(entry.get_time(), entry.__class__.__name__) for entry in self.events]
