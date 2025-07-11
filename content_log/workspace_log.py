from datetime import datetime

from content_log.file_log import FileLog
from event_log.event import Event
from event_log.event_log import EventLog
from event_log.series.time_series import TimeSeries
from processor.learning_goal.learning_goal import LearningGoal

# from event_log.series.progression_with_datetime import ProgressionWithDatetime


class WorkspaceLog(EventLog):
    """
    A collection of file logs
    """

    def __init__(self, file_logs: list[FileLog]):
        self.file_logs = file_logs

        self.check_invariants()

    def check_invariants(self):
        for file_log in self.file_logs:
            file_log.check_invariants()

    def get_events(self) -> list[Event]:
        """
        Get all (time, event_type) pairs of the file log
        """
        sequence: list[Event] = []

        for file_log in self.file_logs:
            sequence.extend(file_log.get_events())

        sequence.sort(key=lambda x: x.get_time())

        return sequence

    def get_amount_of_files(self) -> int:
        return len(self.file_logs)

    def get_file_logs(self) -> list[FileLog]:
        return self.file_logs

    def get_event_sequence(self) -> list[tuple[datetime, str]]:
        """
        Get all (time, event_type) pairs of the files and the chats
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

        return closest_file

    def get_first_accessed_file_after(self, time: datetime):
        """
        Get the file that is first accessed after a certain time
        """

        closest_time = None
        closest_file = None
        for file_log in self.file_logs:
            for event in file_log.get_editing_log().get_events():
                if event.get_time() < time:
                    continue

                if closest_time is None or event.get_time() < closest_time:
                    closest_time = event.get_time()
                    closest_file = file_log


        return closest_file

    def get_learning_goals_progression(
        self, learning_goals: list[LearningGoal]
    ) -> list[TimeSeries]:
        """
        Get the learning goal progression of the file logs for multiple learning goals.
        """

        progressions = [TimeSeries([]) for _ in learning_goals]
        for file_log in self.file_logs:
            progressions_file_log = file_log.get_learning_goals_progression(
                learning_goals
            )
            for index in range(len(learning_goals)):
                progressions[index] = progressions[
                    index
                ].combine_through_concattenation(progressions_file_log[index])

        return progressions
