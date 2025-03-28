from datetime import datetime

from content_log.file_log import FileLog


class WorkspaceLog:
    def __init__(self, file_logs: list[FileLog]):
        self.file_logs = file_logs

    def get_amount_of_files(self) -> int:
        return len(self.file_logs)

    def get_file_logs(self) -> list[FileLog]:
        return self.file_logs

    def get_event_sequence(self) -> list[tuple[datetime, str]]:
        """
        Get all (time, event_type) pairs of the notebook and the chat
        """

        sequence: list[tuple[datetime, str]] = []
        for file_log in self.file_logs:
            sequence.extend(file_log.get_event_sequence())

        sequence.sort(key=lambda x: x[0])

        return sequence

    def get_active_file_at(self, time: datetime):
        """
        Get the active file at a certain time
        """

        closest_time = None
        closest_file = None
        for file_log in self.file_logs:
            for entry in file_log.get_editing_log().get_events():
                if entry.get_time() > time and (
                    closest_time is None or entry.get_time() < closest_time
                ):
                    closest_time = entry.get_time()
                    closest_file = file_log
                    break

        if closest_file is not None:
            return closest_file

        raise ValueError("Time before first event")
