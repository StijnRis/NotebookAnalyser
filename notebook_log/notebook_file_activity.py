from datetime import datetime
from functools import lru_cache
from typing import List

from notebook_log.notebook_activity import NotebookActivity
from notebook_log.notebook_cell_activity import NotebookCellActivity
from notebook_log.notebook_content.notebook_content import NotebookContent
from notebook_log.notebook_log_entry import NotebookLogEntry
from notebook_log.progression.notebook_progression_with_datetime import (
    NotebookProgressionWithDatetime,
)


class NotebookFileActivity(NotebookActivity):
    """
    Activity of one notebook file.
    """

    def __init__(self, log_entries: List[NotebookLogEntry]):
        super().__init__(log_entries)
        self.idle_threshold_seconds = 3600

    def check_invariants(self):
        super().check_invariants()

        # Check that the log entries are for the same file
        for entry in self.log_entries:
            assert (
                entry.notebookState.notebookPath
                == self.log_entries[0].notebookState.notebookPath
            ), "Log entries should be for the same notebook file"

    def get_file_path(self):
        return self.log_entries[0].notebookState.notebookPath

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
        for entry in self.log_entries:
            current_notebook_content = entry.notebookState.notebookContent

            # Check if this event happened
            if entry.eventDetail.eventTime > time:
                continue

            # Check if entire notebook is saved
            if current_notebook_content is not None:
                notebook_content = current_notebook_content
            else:
                print(f"Unknown how to parse {entry.eventDetail.eventName} event")

        return notebook_content

    @lru_cache(maxsize=None)
    def get_progressions(self):
        """
        Calculate the progression of the notebook
        """
        saved_contents = self.get_all_saved_notebook_contents()

        times: list[datetime] = []
        ast_progression: list[float] = []
        output_progression: list[float] = []
        code_progression: list[float] = []

        # Check if user has saved any notebook content
        if len(saved_contents) == 0:
            return (
                NotebookProgressionWithDatetime(times, ast_progression),
                NotebookProgressionWithDatetime(times, output_progression),
                NotebookProgressionWithDatetime(times, code_progression),
            )

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

        return (
            NotebookProgressionWithDatetime(times, ast_progression),
            NotebookProgressionWithDatetime(times, output_progression),
            NotebookProgressionWithDatetime(times, code_progression),
        )

    # TODO make protection against changes the index of a cell
    def get_notebook_cell_activities(self):
        cell_index_to_activity: dict[int, List[NotebookLogEntry]] = {}  

        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName

            eventInfo = entry.eventDetail.eventInfo
            if eventInfo is None:
                print(f"No event info found for {event_name}")
                continue

            if eventInfo.cells is not None:
                cells = eventInfo.cells
                cell_ids = [cell.index for cell in cells]
            else:
                cell_ids = [eventInfo.index]
                if cell_ids[0] is None:
                    print(f"No cell index found for {event_name}")
                    continue

            for cell_id in cell_ids:
                if cell_id not in cell_index_to_activity:
                    cell_index_to_activity[cell_id] = []

                cell_index_to_activity[cell_id].append(entry)

        notebook_cell_activities = []
        for cell_id, entries in cell_index_to_activity.items():
            notebook_cell = self.notebook.get_cell_by_id(cell_id)
            assert notebook_cell is not None, "Notebook cell not found"
            notebook_cell_activities.append(
                NotebookCellActivity(notebook_cell, entries)
            )
