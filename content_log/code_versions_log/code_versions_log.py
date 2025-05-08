import code
from datetime import datetime
from functools import lru_cache
from typing import Sequence

from content_log.code_versions_log.code_file import CodeFile
from event_log.event_log import EventLog
from event_log.series.time_series import TimeSeries
from processor.learning_goal.learning_goal import LearningGoal


class CodeVersionsLog(EventLog):
    def __init__(self, code_file: list[CodeFile]):
        self.code_files = code_file

        self.code_files.sort(key=lambda workspace: workspace.get_time())

        self.check_invariants()

    def check_invariants(self):
        for i in range(len(self.code_files) - 1):
            assert self.code_files[i].get_time() <= self.code_files[i + 1].get_time()

        for i in range(len(self.code_files) - 1):
            assert self.code_files[i].get_path() == self.code_files[i + 1].get_path()

        # for file in self.code_files:
        #     file.check_invariants()

    def get_events(self):
        sequence: Sequence[CodeFile] = []

        sequence.extend(self.code_files)

        sequence.sort(key=lambda x: x.get_time())

        return sequence

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
        
        # if closest_code_file.get_time() != time:
        #     print(f"Code file not found at time {time}, using file at time {closest_code_file.get_time()}")

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

    @lru_cache(maxsize=1)
    def get_code_progression(self):
        saved_workspaces = self.get_code_files()

        data: list[tuple[datetime, float]] = []

        # Check if user has saved any workspaces
        if len(saved_workspaces) == 0:
            return TimeSeries(data)

        last_workspace = saved_workspaces[-1]

        for workspace in saved_workspaces:
            code_difference = workspace.get_code_difference_ratio(last_workspace)

            data.append((workspace.get_time(), code_difference))

        return TimeSeries(data)

    def get_learning_goals_applied_between(
        self, start: datetime, end: datetime, learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        """
        Get the learning goals applied between two datetime points.
        """
        previous_code_version = self.get_code_file_at(start)
        code_version = self.get_code_file_at(end)

        lines_changed = code_version.get_line_numbers_of_new_code(previous_code_version)

        return code_version.get_learning_goals_applied_on_lines(
            lines_changed, learning_goals
        )
