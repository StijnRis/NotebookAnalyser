from datetime import datetime
from typing import List, Optional

from notebook_log.notebook_content.notebook_content import NotebookContent
from notebook_log.notebook_log_entry import NotebookEventName, NotebookLogEntry


class NotebookActivity:
    """
    A collection of log entries for a notebook.
    """

    def __init__(
        self,
        log_entries: List[NotebookLogEntry],
    ):
        self.log_entries = log_entries

        self.log_entries.sort(key=lambda x: x.eventDetail.eventTime)

        self.check_invariants()

    def check_invariants(self):
        # Check that the log entries are sorted by time
        for i in range(1, len(self.log_entries)):
            assert (
                self.log_entries[i].eventDetail.eventTime
                >= self.log_entries[i - 1].eventDetail.eventTime
            ), "Log entries should be sorted by event time"

    def get_start_time(self):
        for entry in self.log_entries:
            if entry.eventDetail.eventName not in [
                "NotebookVisibleEvent",
                "NotebookHiddenEvent",
            ]:
                return entry.eventDetail.eventTime
        assert False, "No event found"

    def get_end_time(self):
        for entry in reversed(self.log_entries):
            if entry.eventDetail.eventName not in [
                "NotebookVisibleEvent",
                "NotebookHiddenEvent",
            ]:
                return entry.eventDetail.eventTime
        assert False, "No event found"

    def get_completion_time(self):
        """
        Get the time it took to complete the notebook.
        """

        return self.get_end_time() - self.get_start_time()

    def get_editing_time(self):
        """
        Calculate the total time spent actively editing the notebook.
        """

        active_time = 0
        last_edit_time = None

        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName
            event_time = entry.eventDetail.eventTime

            if event_name in [
                NotebookEventName.CELL_EDIT,
                NotebookEventName.NOTEBOOK_VISIBLE,
            ]:
                if last_edit_time is not None:
                    active_time += (event_time - last_edit_time).total_seconds()
                last_edit_time = event_time
            elif event_name == NotebookEventName.NOTEBOOK_HIDDEN:
                last_edit_time = None

        return active_time

    def get_cell_indexes(self):
        """
        Get indexes of the cells which are used in this activity
        """

        ids = set()

        for entry in self.log_entries:
            eventInfo = entry.eventDetail.eventInfo
            if eventInfo is None:
                continue

            cell_id = eventInfo.index
            if cell_id is None:
                continue

            ids.add(cell_id)

        return ids

    def get_cell_ids(self):
        """
        Get ids of cells with indexes found in get cell indexes
        """

        ids = set()
        indexes = self.get_cell_indexes()

        for entry in self.log_entries:
            eventInfo = entry.eventDetail.eventInfo
            if eventInfo is None:
                continue
            if eventInfo.cells is not None:
                for cell in eventInfo.cells:
                    if cell.index in indexes:
                        ids.add(cell.id)

        return ids

    def get_amount_of_executions(self):
        total = 0
        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName
            if event_name == NotebookEventName.CELL_EXECUTE:
                total += 1

        return total

    def get_amount_of_events(self):
        return len(self.log_entries)

    def get_event_by_index(self, index: int) -> Optional[NotebookLogEntry]:
        if 0 <= index < len(self.log_entries):
            return self.log_entries[index]
        return None

    def get_amount_of_runtime_errors(self):
        total = 0
        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName
            if event_name == NotebookEventName.CELL_EXECUTE:
                eventInfo = entry.eventDetail.eventInfo
                assert eventInfo is not None, "eventInfo should not be None"
                if eventInfo.success == False:
                    total += 1

        return total

    def get_amount_of_tab_switches(self):
        total = 0
        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName
            event_time = entry.eventDetail.eventTime
            if (
                event_name == NotebookEventName.NOTEBOOK_VISIBLE
                and event_time >= self.get_start_time()
                and event_time <= self.get_end_time()
            ):
                total += 1

        return total

    def get_amount_of_edit_cycles(self):
        """
        Get how many times is the program run and then edited
        """

        total = 0
        edited = False
        for entry in self.log_entries:
            event_name = entry.eventDetail.eventName
            if event_name == NotebookEventName.CELL_EXECUTE and edited:
                total += 1
                edited = False
            if event_name in [
                NotebookEventName.CELL_EDIT,
                NotebookEventName.NOTEBOOK_VISIBLE,
            ]:
                edited = True

        return total

    def get_event_sequence(self):
        """
        Returns a list of tuples with the event time and event name.
        """

        return [
            (entry.eventDetail.eventTime, entry.eventDetail.eventName)
            for entry in self.log_entries
        ]

    def get_all_saved_notebook_contents(self):
        """
        Returns a list of tuples with the event time and notebook content.
        """
        notebook_contents: List[tuple[datetime, NotebookContent]] = []
        for entry in self.log_entries:
            if entry.notebookState.notebookContent is not None:
                notebook_contents.append(
                    (entry.eventDetail.eventTime, entry.notebookState.notebookContent)
                )

        return notebook_contents
    
    def get_active_file_at(self, time: datetime):
        """
        Get the active file at a certain time
        """

        files = self.split_by_file()

        for entry in self.log_entries:
            if entry.eventDetail.eventTime > time:
                path = entry.notebookState.notebookPath
                for file in files:
                    if file.get_file_path() == path:
                        return file

        raise ValueError("Time before first event")

    def split_by_file(self):
        """
        Split the notebook activity into activity per file
        """
        from notebook_log.notebook_file_activity import NotebookFileActivity

        files = {}
        for entry in self.log_entries:
            path = entry.notebookState.notebookPath
            if path not in files:
                files[path] = []
            files[path].append(entry)

        activities = [NotebookFileActivity(file) for file in files.values()]

        return activities

    
