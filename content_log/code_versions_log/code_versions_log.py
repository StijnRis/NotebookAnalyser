from datetime import datetime
from functools import lru_cache

from content_log.code_versions_log.code_file import CodeFile
from content_log.progression.progression_with_datetime import ProgressionWithDatetime
from processor.learning_goal.learning_goal import LearningGoal


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

        closest_code_file = None
        for code_file in self.code_files:
            if code_file.get_time() > time:
                break
            closest_code_file = code_file

        if closest_code_file is None:
            return CodeFile(time, "", "")

        return closest_code_file

    def remove_duplicates(self):
        """
        Remove duplicate code files.
        """

        new_code_files: list[CodeFile] = []
        for code_file in self.code_files:
            if (
                len(new_code_files) == 0
                or new_code_files[-1].get_code() != code_file.get_code()
            ):
                new_code_files.append(code_file)

        return CodeVersionsLog(new_code_files)

    @lru_cache(maxsize=None)
    def get_code_progression(self):
        saved_workspaces = self.get_code_files()

        times: list[datetime] = []
        code_progression: list[float] = []

        # Check if user has saved any workspaces
        if len(saved_workspaces) == 0:
            return ProgressionWithDatetime(times, code_progression)

        last_workspace = saved_workspaces[-1]

        for workspace in saved_workspaces:
            code_difference = workspace.get_code_difference_ratio(last_workspace)

            times.append(workspace.get_time())
            code_progression.append(code_difference)

        return ProgressionWithDatetime(times, code_progression)

    def get_learning_goals_applied_between(
        self, start: datetime, end: datetime, learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        """
        Get the learning goals applied between two datetime points.
        """
        previous_code_version = self.get_code_file_at(start)
        code_version = self.get_code_file_at(end)

        lines_changed = code_version.get_line_numbers_of_new_code(previous_code_version)
        new_ast_items = code_version.get_ast_of_lines(lines_changed)

        learning_goals_in_ast = []
        for ast_item in new_ast_items:
            for goal in learning_goals:
                if goal.is_applied_in(ast_item):
                    learning_goals_in_ast.append(goal)

        return learning_goals_in_ast
