from datetime import datetime, timedelta
from difflib import unified_diff

from content_log.code_versions_log.code_versions_log import CodeVersionsLog
from content_log.event_log.events_log import EditingLog
from content_log.execution_log.execution_result import ExecutionErrorResult
from content_log.execution_log.file_execution_log import FileExecutionLog


class FileLog:
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

    def get_active_periods(self) -> list[tuple[datetime, datetime]]:
        event_sequence = self.get_event_sequence()

        active_periods: list[tuple[datetime, datetime]] = []
        start_time = None
        previous_time = None
        for event in event_sequence:
            event_time = event[0]
            if start_time is None or previous_time is None:
                start_time = event_time
            elif (event_time - previous_time) > self.idle_threshold:
                active_periods.append((start_time, event_time))
                start_time = None

            previous_time = event_time

        if start_time is not None:
            active_periods.append((start_time, event_sequence[-1][0]))

        return active_periods

    def get_event_sequence(self) -> list[tuple[datetime, str]]:
        editing_sequence = self.editing_log.get_event_sequence()
        execution_sequence = self.file_execution_log.get_event_sequence()

        event_sequence = editing_sequence + execution_sequence

        event_sequence.sort(key=lambda x: x[0])

        return event_sequence

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
