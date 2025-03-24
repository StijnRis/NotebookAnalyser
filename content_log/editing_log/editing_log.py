from datetime import datetime, timedelta
from typing import List

from content_log.editing_log.editing_event import (
    EditEvent,
    EditingEvent,
    ExecuteEvent,
    FileHiddenEvent,
    FileVisibleEvent,
)


class EditingLog:
    """
    A collection of editing events
    """

    def __init__(
        self,
        events: List[EditingEvent],
    ):
        self.events = events
        self.idle_threshold = timedelta(minutes=5)

        self.events.sort(key=lambda x: x.get_time())

        self.check_invariants()

    def check_invariants(self):
        # Check that the log entries are sorted by time
        for i in range(1, len(self.events)):
            assert (
                self.events[i].get_time() >= self.events[i - 1].get_time()
            ), "Log entries should be sorted by event time"

    def get_events(self):
        return self.events

    def get_start_time(self):
        for entry in self.events:
            if not isinstance(entry, (FileVisibleEvent, FileHiddenEvent)):
                return entry.get_time()
        print("No start time found")
        return datetime.fromtimestamp(0)

    def get_end_time(self):
        for entry in reversed(self.events):
            if not isinstance(entry, (FileVisibleEvent, FileHiddenEvent)):
                return entry.get_time()
        print("No end time found")
        return datetime.fromtimestamp(0)

    def get_completion_time(self):
        """
        Get time between the first and last event
        """

        return self.get_end_time() - self.get_start_time()

    def get_open_time(self) -> timedelta:
        """
        Calculate the total time of having a file open
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

    def get_total_editing_time(self) -> timedelta:
        """
        Calculate the total time of editing
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

    def get_editing_periods(self) -> list[tuple[datetime, datetime]]:
        """
        Get the start and end times of every period of editing activity.
        """
        visible_periods: list[tuple[datetime, datetime]] = []
        start_time = None

        for entry in self.events:

            if isinstance(entry, FileVisibleEvent):
                if start_time is None:
                    start_time = entry.get_time()
            elif isinstance(entry, FileHiddenEvent):
                if start_time is not None:
                    end_time = entry.get_time()
                    visible_periods.append((start_time, end_time))
                    start_time = None

        # If the notebook is still visible at the end of the log
        if start_time is not None:
            visible_periods.append((start_time, self.events[-1].get_time()))

        return visible_periods

    def get_amount_of_events(self):
        return len(self.events)

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

    def get_amount_of_edit_cycles(self):
        """
        Get how many times is the program run and then edited
        """

        total = 0
        edited = False
        for entry in self.events:
            if isinstance(entry, ExecuteEvent) and edited:
                total += 1
                edited = False
            if isinstance(entry, EditEvent):
                edited = True

        return total
