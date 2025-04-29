from datetime import datetime, timedelta
from difflib import unified_diff

from content_log.code_versions_log.code_versions_log import CodeVersionsLog
from content_log.event_log.events_log import EditingLog
from content_log.execution_log.execution_result import ExecutionErrorResult
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

    # TODO remove
    def get_code_fix_for_error(self, error: ExecutionErrorResult) -> str:
        """
        Get the changes made to the code after a runtime error.
        This is done by comparing the code of the error and after the error.
        """
        time = error.get_time()
        fixed_execution = self.file_execution_log.get_first_successful_execution_after(
            time
        )

        if fixed_execution is None:
            return "No fix"

        code_file = self.code_version_log.get_code_file_at(time)
        code_file_after = self.code_version_log.get_code_file_at(
            fixed_execution.get_time()
        )
        code_file = code_file.get_code()
        code_file_after = code_file_after.get_code()

        differences = "\n".join(
            unified_diff(
                code_file.splitlines(), code_file_after.splitlines(), lineterm=""
            )
        )

        return differences

    # TODO merge with executing analyser (Now it is duplicated)
    def get_learning_goals_progression(
        self, learning_goals: list[LearningGoal]
    ) -> list[TimeSeries]:
        """
        Get the learning goal progression for a certain learning goal.
        """
        datas = [[] for _ in learning_goals]

        previous_successful_execution = None
        errors_before_succes: list[ExecutionErrorResult] = []
        for execution in self.file_execution_log.get_executions():
            if isinstance(execution, ExecutionErrorResult):
                errors_before_succes.append(execution)
                continue

            if previous_successful_execution is None:
                previous_successful_execution = execution
                continue

            time = execution.get_time()

            applied_learning_goals = (
                self.code_version_log.get_learning_goals_applied_between(
                    previous_successful_execution.get_time(), time, learning_goals
                )
            )

            for index, learning_goal in enumerate(learning_goals):
                amount_of_times_applied = applied_learning_goals.count(learning_goal)
                if amount_of_times_applied > 0:
                    datas[index].append((time, 1 if len(errors_before_succes) == 0 else -1))

            previous_successful_execution = execution
            errors_before_succes = []

        result = []
        for index, goal in enumerate(learning_goals):
            result.append(TimeSeries(datas[index]))
        return result
