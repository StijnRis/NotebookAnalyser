from datetime import datetime
from functools import lru_cache

from content_log.code.file_versions_log import CodeVersionsLog
from content_log.editing_log.editing_log import EditingLog
from content_log.execution_log.file_execution_log import FileExecutionLog
from content_log.progression.progression_with_datetime import ProgressionWithDatetime


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

    def get_path(self) -> str:
        return self.path

    def get_editing_log(self) -> EditingLog:
        return self.editing_log

    def get_code_version_log(self) -> CodeVersionsLog:
        return self.code_version_log

    def get_file_execution_log(self) -> FileExecutionLog:
        return self.file_execution_log

    def get_start_time(self) -> datetime:
        time1 = self.editing_log.get_start_time()
        time2 = self.code_version_log.get_start_time()
        time3 = self.file_execution_log.get_start_time()

        return max(time1, time2, time3)

    def get_end_time(self) -> datetime:
        time1 = self.editing_log.get_end_time()
        time2 = self.code_version_log.get_end_time()
        time3 = self.file_execution_log.get_end_time()

        return max(time1, time2, time3)

    @lru_cache(maxsize=None)
    def get_ast_progression(self):
        files = self.get_code_version_log().get_code_files()

        times: list[datetime] = []
        ast_progression: list[float] = []

        # Check if user has saved any notebook content
        if len(files) == 0:
            return ProgressionWithDatetime(times, ast_progression)

        last_file = files[-1]

        for file in files:
            ast_difference = file.get_ast_difference_ratio(last_file)

            times.append(file.get_time())
            ast_progression.append(ast_difference)

        return ProgressionWithDatetime(times, ast_progression)

    @lru_cache(maxsize=None)
    def get_code_progression(self):
        saved_workspaces = self.get_code_version_log().get_code_files()

        times: list[datetime] = []
        code_progression: list[float] = []

        # Check if user has saved any notebook content
        if len(saved_workspaces) == 0:
            return ProgressionWithDatetime(times, code_progression)

        last_workspace = saved_workspaces[-1]

        for workspace in saved_workspaces:
            code_difference = workspace.get_code_difference_ratio(last_workspace)

            times.append(workspace.get_time())
            code_progression.append(code_difference)

        return ProgressionWithDatetime(times, code_progression)

    @lru_cache(maxsize=None)
    def get_output_progression(self):
        execution_outputs = self.get_file_execution_log().get_execution_outputs()

        times: list[datetime] = []
        output_progression: list[float] = []

        # Check if user has saved any notebook content
        if len(execution_outputs) == 0:
            return ProgressionWithDatetime(times, output_progression)

        last_execution_output = execution_outputs[-1]

        for execution_output in execution_outputs:
            output_similarity = execution_output.get_output_similarity_ratio(
                last_execution_output
            )

            times.append(execution_output.get_time())
            output_progression.append(output_similarity)

        return ProgressionWithDatetime(times, output_progression)

    def get_event_sequence(self) -> list[tuple[datetime, str]]:
        editing_sequence = self.editing_log.get_event_sequence()
        execution_sequence = self.file_execution_log.get_event_sequence()

        return editing_sequence + execution_sequence
