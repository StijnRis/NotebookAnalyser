from abc import ABC, abstractmethod
from datetime import datetime
from difflib import SequenceMatcher
from functools import lru_cache
import re

from content_log.execution_log.analyser.execution_error_result_analyser import (
    ExecutionErrorResultAnalyser,
    LearningGoal,
)
from event_log.event import Event


class ExecutionResult(Event, ABC):
    def __init__(self, time: datetime):
        self.time = time

    def get_time(self) -> datetime:
        return self.time

    @abstractmethod
    def get_content(self) -> str:
        pass

    def get_output_similarity_ratio(self, other: "ExecutionResult"):
        """
        Compare output of two files
        """

        output1 = self.get_content()
        output2 = other.get_content()

        return SequenceMatcher(None, output1, output2).ratio()

class ExecutionSuccessResult(ExecutionResult, ABC):
    pass

class ExecutionEmptyResult(ExecutionSuccessResult):
    def __init__(self, time: datetime):
        super().__init__(time)

    def get_content(self) -> str:
        return "<EmptyResult>"


class ExecutionStreamResult(ExecutionSuccessResult):
    """
    "output_type": "stream"
    """

    def __init__(self, time: datetime, content: str):
        super().__init__(time)
        self.content = content

    def get_content(self) -> str:
        return self.content

class ExecutionTextResult(ExecutionSuccessResult):
    def __init__(self, time: datetime, result: dict):
        super().__init__(time)
        self.result = result

    def get_content(self) -> str:
        return str(self.result)


class ExecutionImageResult(ExecutionSuccessResult):
    def __init__(self, time: datetime, data: dict):
        super().__init__(time)
        self.data = data

    def get_content(self) -> str:
        return "DisplayDataResult"

class ExecutionErrorResult(ExecutionResult):
    def __init__(
        self,
        time: datetime,
        traceback: str,
        error_name: str,
        error_value: str,
        analyser: ExecutionErrorResultAnalyser,
    ):
        super().__init__(time)
        self.traceback = traceback
        self.error_name = error_name
        self.error_value = error_value
        self.analyser = analyser

    def get_traceback(self) -> str:
        return self.traceback

    def get_cleaned_traceback(self) -> str:
        traceback = self.traceback
        traceback = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', traceback)
        return traceback

    def get_error_name(self) -> str:
        return self.error_name

    def get_error_value(self) -> str:
        return self.error_value

    def get_content(self) -> str:
        return f"{self.error_name}: {self.error_value}"

    @lru_cache(maxsize=None)
    def get_error_type(self) -> LearningGoal:
        return self.analyser.get_error_type(self)