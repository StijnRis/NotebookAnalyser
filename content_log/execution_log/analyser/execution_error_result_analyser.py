from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from processor.learning_goal import LearningGoal



if TYPE_CHECKING:
    from content_log.execution_log.execution_result import ExecutionErrorResult


class ExecutionErrorResultAnalyser(ABC):

    def __init__(self, error_types: list[LearningGoal]):
        self.error_types = error_types

    @abstractmethod
    def get_error_type(self, error_event: "ExecutionErrorResult") -> "LearningGoal":
        pass
