from datetime import datetime
from functools import lru_cache
from typing import List

from editing_log.builder.notebook_log_entry import NotebookEventName, NotebookLogEntry
from editing_log.content_event import ContentEvent
from editing_log.editing_content_activity import EditingContentActivity



class EditingFileActivity(EditingContentActivity):
    """
    Coding activity of a single file.
    """

    def __init__(self, events: List[ContentEvent], file_path: str):
        super().__init__(events)
        self.file_path = file_path

    def get_file_path(self):
        return self.file_path

    

    # TODO make protection against changes the index of a cell
    def get_notebook_cell_activities(self):
        cell_index_to_activity: dict[int, List[NotebookLogEntry]] = {}

        for entry in self.events:
            event_name = entry.eventDetail.eventName

            eventInfo = entry.eventDetail.eventInfo
            if eventInfo is None:
                print(f"No event info found for {event_name}")
                continue

            if eventInfo.cells is not None:
                cells = eventInfo.cells
                cell_ids = [cell.index for cell in cells]
            else:
                if eventInfo.index is None:
                    print(f"No cell index found for {event_name}")
                    continue
                cell_ids = [eventInfo.index]

            for cell_id in cell_ids:
                if cell_id not in cell_index_to_activity:
                    cell_index_to_activity[cell_id] = []

                cell_index_to_activity[cell_id].append(entry)

        notebook_cell_activities: list[CodeSnippetActivity] = []
        for cell_id, entries in cell_index_to_activity.items():
            notebook_cell_activities.append(CodeSnippetActivity(entries))

        return notebook_cell_activities

    def get_visible_periods(self):
        """
        Get the start and end times of every period this file was visible.
        """
        visible_periods: list[tuple[datetime, datetime]] = []
        start_time = None

        for entry in self.events:
            event_name = entry.eventDetail.eventName

            if event_name == NotebookEventName.NOTEBOOK_VISIBLE:
                if start_time is None:
                    start_time = entry.eventDetail.eventTime
            elif event_name == NotebookEventName.NOTEBOOK_HIDDEN:
                if start_time is not None:
                    end_time = entry.eventDetail.eventTime
                    visible_periods.append((start_time, end_time))
                    start_time = None

        # If the notebook is still visible at the end of the log
        if start_time is not None:
            visible_periods.append((start_time, self.events[-1].eventDetail.eventTime))

        return visible_periods
