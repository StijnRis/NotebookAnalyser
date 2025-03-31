from datetime import datetime

from content_log.file_log import FileLog


class WorkspaceLog:
    def __init__(self, file_logs: list[FileLog]):
        self.file_logs = file_logs

        self.check_invariants()
    
    def check_invariants(self):
        for file_log in self.file_logs:
            file_log.check_invariants()

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
            for event in file_log.get_editing_log().get_events():
                if event.get_time() > time:
                    break

                if closest_time is None or event.get_time() > closest_time:
                    closest_time = event.get_time()
                    closest_file = file_log

        if closest_file is None:
            raise ValueError("Time before first event")
        
        return closest_file

        
