from datetime import datetime
from typing import List

from notebook_log.notebook_activity import NotebookActivity
from notebook_log.notebook_log_entry import NotebookLogEntry


class NotebookFileActivity(NotebookActivity):
    """
    Activity of a specific notebook file.
    """

    def __init__(
        self,
        log_entries: List[NotebookLogEntry],
    ):
        super().__init__(log_entries)

    def check_invariants(self):
        super().check_invariants()

        # Check that the log entries are for the same file
        for entry in self._log_entries:
            assert (
                entry.notebookState.notebookPath
                == self._log_entries[0].notebookState.notebookPath
            ), "Log entries should be for the same notebook file"

    def get_file_path(self):
        return self._log_entries[0].notebookState.notebookPath
    
    def get_progressions(self):
        """
        Calculate the progression of notebook content over time.
        """
        saved_contents = self.get_all_saved_notebook_contents()

        times = []
        ast_progression = []
        output_progression = []
        code_progression = []

        # Check if user has saved any notebook content
        if len(saved_contents) == 0:
            return times, ast_progression, output_progression, code_progression

        last_notebook_content = saved_contents[-1][1]

        for event_time, content in saved_contents:
            ast_difference = content.get_ast_difference_ratio(last_notebook_content)

            output_difference = content.get_output_difference_ratio(
                last_notebook_content
            )

            code_difference = content.get_code_difference_ratio(last_notebook_content)

            times.append(event_time)
            ast_progression.append(ast_difference)
            output_progression.append(output_difference)
            code_progression.append(code_difference)

        return times, ast_progression, output_progression, code_progression

    def get_notebook_cell_content_at(self, cell_id: str, time: datetime):
        """
        Get the content of a notebook cell at a certain time.
        """

        notebook_content = self.get_notebook_content_at(time)

        # Check if there is notebook content
        if notebook_content is not None:
            cells = notebook_content.cells
            for cell in cells:
                if cell.id == cell_id:
                    return cell

        return None

    def get_notebook_content_at(self, time: datetime):
        """
        Get the notebook content at a certain time.
        """
        notebook_content = None

        # Loop through all events
        for entry in self._log_entries:
            current_notebook_content = entry.notebookState.notebookContent

            # Check if this event happened
            if entry.eventDetail.eventTime > time:
                continue

            # Check if entire notebook is saved
            if current_notebook_content is not None:
                notebook_content = current_notebook_content

            print(f"Unknown how to parse {entry.eventDetail.eventName} event")

        return notebook_content
