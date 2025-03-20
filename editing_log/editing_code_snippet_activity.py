from typing import List

from editing_log.content_event import ContentEvent
from editing_log.editing_content_activity import EditingContentActivity


class EditingCodeSnippetActivity(EditingContentActivity):
    """
    All content activities that happend for a single code snippet (notebook cell).
    """

    def __init__(
        self,
        log_entries: List[ContentEvent],
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
