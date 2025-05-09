from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from content_log.code_versions_log.code_file import CodeFile
from processor.learning_goal.learning_goal import LearningGoal

if TYPE_CHECKING:
    from content_log.execution_log.execution_result import ExecutionErrorResult


class ExecutionErrorResultAnalyser(ABC):

    def __init__(self, learning_goals: list[LearningGoal]):
        self.learning_goals = learning_goals

    @abstractmethod
    def get_error_type(
        self, error_event: "ExecutionErrorResult", code_file: CodeFile
    ) -> "LearningGoal":
        pass
