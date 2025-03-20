from datetime import datetime
from typing import List

from editing_log.editing_content_activity import EditingContentActivity


class EditingWorkspaceActivity(EditingContentActivity):
    """
    Coding activity of multiple files.
    """

    def __init__(self, events: List[ContentEvent]):
        super().__init__(events)

    def get_active_file_at(self, time: datetime):
        """
        Get the active file at a certain time
        """

        files = self.split_by_file()

        for entry in self.events:
            if entry.eventDetail.eventTime > time:
                path = entry.notebookState.notebookPath
                for file in files:
                    if file.get_file_path() == path:
                        return file

        raise ValueError("Time before first event")
    
    def split_by_file(self):
        """
        Split the content activity into activity per file
        """
        from content_log.file_activity import FileActivity

        files = {}
        for entry in self.events:
            path = entry.notebookState.notebookPath
            if path not in files:
                files[path] = []
            files[path].append(entry)

        activities = [FileActivity(file) for file in files.values()]

        return activities