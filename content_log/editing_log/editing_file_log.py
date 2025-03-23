from typing import List

from content_log.editing_log.editing_event import EditingEvent
from content_log.editing_log.editing_log import EditingLog


class EditingFileLog(EditingLog):
    """
    Coding activity of a single file. (We see each notebook cell as a single file)
    """

    def __init__(self, file_path: str, events: List[EditingEvent]):
        self.file_path = file_path
        super().__init__(events)

    def get_file_path(self):
        return self.file_path
