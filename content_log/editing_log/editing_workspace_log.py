from datetime import datetime

from file_log.editing_log.editing_file_log import EditingFileLog

from file_log.editing_log.editing_log import EditingLog


class EditingWorkspaceLog(EditingLog):
    """
    Coding activity of multiple files.
    """

    def __init__(self, files: list[EditingFileLog]):
        self.files = files
        events = [event for file in files for event in file.events]
        super().__init__(events)

    def get_active_file_at(self, time: datetime):
        """
        Get the active file at a certain time
        """

        closest_time = None
        closest_file = None
        for file in self.files:
            for entry in self.events:
                if entry.get_time() > time and (
                    closest_time is None or entry.get_time() < closest_time
                ):
                    closest_time = entry.get_time()
                    closest_file = file
                    break

        if closest_file is not None:
            return closest_file

        raise ValueError("Time before first event")

    def get_file_activities(self):
        return self.files
