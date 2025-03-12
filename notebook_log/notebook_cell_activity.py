from datetime import datetime
from difflib import SequenceMatcher
from typing import List

from notebook_log.notebook_activity import NotebookActivity
from notebook_log.notebook_content.notebook_content_cell import NotebookContentCell
from notebook_log.notebook_log_entry import NotebookLogEntry


class NotebookCellActivity(NotebookActivity):
    """
    All notebook activities that happend in a single notebook cell.
    """

    def __init__(
        self,
        log_entries: List[NotebookLogEntry],
    ):
        super().__init__(log_entries)

    def check_invariants(self):
        super().check_invariants()

        # Check that all cells have the same index
        indexes = self.get_cell_indexes()
        assert len(indexes) == 1, "All cells should have the same index"

        # Check that all cells have the same id
        ids = self.get_cell_ids()
        assert len(ids) == 1, "There should be one cell id"

    def get_cell_id(self):
        ids = self.get_cell_ids()
        assert len(ids) == 1, "There should be one cell id"
        return ids.pop()

    def get_cell_index(self):
        indexes = self.get_cell_indexes()
        assert len(indexes) == 1, "All cells should have the same index"
        return indexes.pop()

    def get_content_at(self, time: datetime):
        """
        Get the notebook content at a certain time.
        """
        cell_content = None
        cell_id = self.get_cell_id()

        # Loop through all events
        for entry in self.log_entries:

            # Check if this event happened
            if entry.eventDetail.eventTime > time:
                continue

            # Check if entire notebook is saved
            current_notebook_content = entry.notebookState.notebookContent
            if current_notebook_content is not None:
                cells = current_notebook_content.cells
                for cell in cells:
                    if cell.id == cell_id:
                        cell_content = cell
            else:
                print(f"Unknown how to parse {entry.eventDetail.eventName} event")

        assert cell_content is not None, "No cell content found"
        return cell_content

    def get_similarity_between_cell_states(self, time1: datetime, time2: datetime):
        end_result = self.get_content_at(time1).get_source()
        current_result = self.get_content_at(time2).get_source()
        return SequenceMatcher(None, end_result, current_result).ratio()

    def get_overview(self, level=1) -> str:
        return (
            f"{'#' * level} Notebook summary of cell {self.get_cell_id()}\n\n"
            f"Worked on from {self.get_start_time()} to {self.get_end_time()}\\\n"
            f"Completion time = {self.get_completion_time()}\\\n"
            f"Tab switches = {self.get_amount_of_tab_switches()}\\\n"
            f"Times executed = {self.get_amount_of_executions()} times\\\n"
            f"Runtime errors = {self.get_amount_of_runtime_errors()}\\\n"
            f"Edit cycles = {self.get_amount_of_edit_cycles()}\\\n"
            f"Similarity between initial and final state = {round(self.get_similarity_between_cell_states(self.get_start_time(), self.get_end_time()), 2)}\\\n"
            f"{'#' * (level + 1)} Initial state\n\n"
            f"```python\n{self.get_content_at(self.get_start_time())}\n```\n\n"
            f"{'#' * (level + 1)} Final state\n\n"
            f"```python\n{self.get_content_at(self.get_end_time())}\n```\n\n"
        )
