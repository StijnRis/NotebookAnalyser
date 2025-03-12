from typing import Dict, List

from notebook_log.notebook_activity import NotebookActivity
from notebook_log.notebook_cell_activity import NotebookCellActivity
from notebook_log.notebook_log_entry import NotebookLogEntry


class NotebookLog(NotebookActivity):
    """
    Log of all notebook activities.
    """

    def __init__(self, log_entries: List[NotebookLogEntry]):
        super().__init__(log_entries)

    
    def get_overview(self, level=1):
        return f"{'#' * level} Notebook activity\n\n" f"None yet"
