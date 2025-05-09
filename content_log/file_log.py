from datetime import datetime, timedelta
from functools import lru_cache

from content_log.code_versions_log.code_versions_log import CodeVersionsLog
from content_log.edit_run_cycle import EditRunCycle
from content_log.event_log.events_log import EditingLog
from content_log.execution_log.file_execution_log import FileExecutionLog
from event_log.event import Event
from event_log.event_log import EventLog
from event_log.series.time_series import TimeSeries
from processor.learning_goal.learning_goal import LearningGoal


class FileLog(EventLog):
    """
    A collection of logs related to a single file.
    """

    def __init__(
        self,
        path: str,
        editing_log: EditingLog,
        code_version_log: CodeVersionsLog,
        file_execution_log: FileExecutionLog,
    ):
        self.path = path
        self.editing_log = editing_log
        self.code_version_log = code_version_log
        self.file_execution_log = file_execution_log
        self.idle_threshold = timedelta(minutes=5)

        self.check_invariants()

    def check_invariants(self):
        self.editing_log.check_invariants()
        self.code_version_log.check_invariants()
        self.file_execution_log.check_invariants()

    def get_events(self):
        """
        Get all (time, event_type) pairs of the file log
        """
        sequence: list[Event] = []

        sequence.extend(self.editing_log.get_events())
        sequence.extend(self.file_execution_log.get_events())
        sequence.extend(self.code_version_log.get_events())

        sequence.sort(key=lambda x: x.get_time())

        return sequence

    def get_path(self) -> str:
        return self.path

    def get_editing_log(self) -> EditingLog:
        return self.editing_log

    def get_code_version_log(self) -> CodeVersionsLog:
        return self.code_version_log

    def get_file_execution_log(self) -> FileExecutionLog:
        return self.file_execution_log

    def get_start_active_time(self) -> datetime:
        time1 = self.editing_log.get_start_active_time()
        time2 = self.code_version_log.get_start_time()
        time3 = self.file_execution_log.get_start_time()

        return max(time1, time2, time3)

    def get_end_active_time(self) -> datetime:
        time1 = self.editing_log.get_end_active_time()
        time2 = self.code_version_log.get_end_time()
        time3 = self.file_execution_log.get_end_time()

        return max(time1, time2, time3)

    def get_start_passive_time(self) -> datetime:
        time1 = self.editing_log.get_start_passive_time()
        time2 = self.code_version_log.get_start_time()
        time3 = self.file_execution_log.get_start_time()

        return max(time1, time2, time3)

    def get_end_passive_time(self) -> datetime:
        time1 = self.editing_log.get_end_passive_time()
        time2 = self.code_version_log.get_end_time()
        time3 = self.file_execution_log.get_end_time()

        return max(time1, time2, time3)

    def get_event_sequence(self) -> list[tuple[datetime, str]]:
        editing_sequence = self.editing_log.get_event_sequence()
        execution_sequence = self.file_execution_log.get_event_sequence()

        event_sequence = editing_sequence + execution_sequence

        event_sequence.sort(key=lambda x: x[0])

        return event_sequence

    @lru_cache(maxsize=None)
    def get_all_edit_run_cycles(self) -> list[EditRunCycle]:
        """
        Get all edit run cycles in the file log.
        """
        edit_run_cycles: list[EditRunCycle] = []

        previous_runned_code = self.code_version_log.get_code_file_at(
            self.code_version_log.get_start_time()
        )
        previous_successful_code = self.code_version_log.get_code_file_at(
            self.code_version_log.get_start_time()
        )
        for execution in self.file_execution_log.get_executions():
            time = execution.get_time()
            code_file = self.code_version_log.get_code_file_at(time)

            edit_run_cycle = EditRunCycle(
                execution, code_file, previous_runned_code, previous_successful_code
            )
            edit_run_cycles.append(edit_run_cycle)

            previous_runned_code = code_file
            if execution.get_error() is None:
                previous_successful_code = code_file

        return edit_run_cycles

    def get_learning_goals_progression(
        self, learning_goals: list[LearningGoal]
    ) -> list[TimeSeries]:
        """
        Get the learning goal progression for a certain learning goal.
        """
        datas = [[] for _ in learning_goals]

        for edit_run_cycle in self.get_all_edit_run_cycles():
            if edit_run_cycle.get_execution().get_error() is None:
                applied_learning_goals = edit_run_cycle.get_applied_learning_goals(learning_goals)
                for index, learning_goal in enumerate(learning_goals):
                    if learning_goal in applied_learning_goals:
                        datas[index].append(
                            (edit_run_cycle.get_execution().get_time(), 1)
                        )
            else:
                applied_learning_goals = edit_run_cycle.get_learning_goals_in_error()
                for error_type in applied_learning_goals:
                    if error_type is not None:
                        index = learning_goals.index(error_type)
                        datas[index].append((edit_run_cycle.get_execution().get_time(), -1))

        result = []
        for index, goal in enumerate(learning_goals):
            result.append(TimeSeries(datas[index]))
        return result
