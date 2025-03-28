from datetime import timedelta
from typing import List

from content_log.event_log.content_event import (
    ContentEvent,
    FileHiddenEvent,
    FileVisibleEvent,
)
from content_log.event_log.events_log import EditingLog


class EditingFileLog(EditingLog):
    """
    Coding activity of a single file. (Each notebook cell is a single file)
    """

    def __init__(self, file_path: str, events: List[ContentEvent]):
        self.file_path = file_path
        super().__init__(events)

    def check_invariants(self):
        super().check_invariants()

        # Check that each file visible event has a corresponding file hidden event
        visible = False
        for event in self.events:
            if isinstance(event, FileVisibleEvent):
                assert not visible, "File already visible"
                visible = True
            elif isinstance(event, FileHiddenEvent):
                assert visible, "File not visible"
                visible = False

    def get_file_path(self):
        return self.file_path

    def get_visible_time(self) -> timedelta:
        """
        Calculate the total time of having a file visible
        """

        visible_time = timedelta(0)
        last_time = None

        for event in self.events:
            event_time = event.get_time()

            if isinstance(event, FileVisibleEvent):
                last_time = event_time

            if isinstance(event, FileHiddenEvent) and last_time is not None:
                visible_time += event_time - last_time
                last_time = None

            last_time = event_time

        return visible_time
