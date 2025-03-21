from typing import List

from content_log.editing_log.editing_code_snippet_log import EditingCodeSnippetLog
from content_log.editing_log.editing_event import EditingEvent
from content_log.editing_log.editing_file_log import EditingFileLog


class EditingNotebookLog(EditingFileLog):
    """
    Coding activity of a single file.
    """

    def __init__(self, file_path: str, events: List[EditingEvent] , code_snippets: List[EditingCodeSnippetLog]):
        self.code_snippets = code_snippets
        super().__init__(file_path, events)

    def get_cell_activities(self):
        return self.code_snippets
