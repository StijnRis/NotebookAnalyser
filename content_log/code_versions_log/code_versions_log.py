from datetime import datetime
from functools import lru_cache

from content_log.code_versions_log.code_file import CodeFile
from content_log.progression.progression_with_datetime import ProgressionWithDatetime


class CodeVersionsLog:
    def __init__(self, code_file: list[CodeFile]):
        self.code_files = code_file

        self.code_files.sort(key=lambda workspace: workspace.get_time())

        self.check_invariants()

    def check_invariants(self):
        for i in range(len(self.code_files) - 1):
            assert self.code_files[i].get_time() <= self.code_files[i + 1].get_time()

        for i in range(len(self.code_files) - 1):
            assert self.code_files[i].get_path() == self.code_files[i + 1].get_path()

        # for workspace in self.workspaces:
        #     workspace.check_invariants()

    def get_code_files(self) -> list[CodeFile]:
        return self.code_files
    
    def get_amount_of_code_files(self) -> int:
        return len(self.code_files)
    
    def get_start_time(self) -> datetime:
        if len(self.code_files) == 0:
            return datetime.fromtimestamp(0)
        return self.code_files[0].get_time()
    
    def get_end_time(self) -> datetime:
        if len(self.code_files) == 0:
            return datetime.fromtimestamp(0)
        return self.code_files[-1].get_time()

    def get_code_file_at(self, time: datetime) -> CodeFile:
        """
        Get the code content at a certain time.
        """

        for code_file in self.code_files:
            if code_file.get_time() >= time:
                return code_file

        return CodeFile(time, "", "")

    def remove_duplicates(self):
        """
        Remove duplicate code files.
        """

        new_code_files: list[CodeFile] = []
        for code_file in self.code_files:
            if len(new_code_files) == 0 or new_code_files[-1].get_code() != code_file.get_code():
                new_code_files.append(code_file)

        return CodeVersionsLog(new_code_files)
    
    @lru_cache(maxsize=None)
    def get_code_progression(self):
        saved_workspaces = self.get_code_files()

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
    def get_ast_progression(self):
        files = self.get_code_files()

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
