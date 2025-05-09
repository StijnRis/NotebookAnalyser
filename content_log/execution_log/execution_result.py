import re
from abc import ABC, abstractmethod
from datetime import datetime
from difflib import SequenceMatcher
from functools import lru_cache

from content_log.code_versions_log.code_file import CodeFile
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
        traceback = re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", traceback)
        # traceback = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", traceback)
        return traceback

    def get_error_name(self) -> str:
        return self.error_name

    def get_error_value(self) -> str:
        return self.error_value

    def get_content(self) -> str:
        return f"{self.error_name}: {self.error_value}\n{self.get_cleaned_traceback()}"

    def get_line_numbers(self) -> list[int]:
        """
        Get the line numbers of the error in the traceback
        """
        traceback = self.get_cleaned_traceback()
        lines = traceback.splitlines()
        line_numbers = []
        for line in lines:
            match = re.search(r"line (\d+)", line)
            if match:
                line_numbers.append(int(match.group(1)))
        return line_numbers

    @lru_cache(maxsize=None)
    def get_error_type(self, code_file: CodeFile) -> LearningGoal:
        # assert code_file.get_time() == self.get_time(), "Code file time does not match error time"
        return self.analyser.get_error_type(self, code_file)

    def has_error_occurred(self) -> bool:
        if self.error_name == "KeyboardInterrupt":
            return False
        return True


class ExecutionCompositeResult(Event):
    def __init__(self, time: datetime, results: list[ExecutionResult]):
        self.time = time
        self.results = results

    def get_time(self) -> datetime:
        return self.time

    def get_content(self) -> str:
        if len(self.results) == 0:
            return "<EmptyResult>"
        return "\n".join([result.get_content() for result in self.results])

    def get_error(self) -> ExecutionErrorResult | None:
        for result in self.results:
            if isinstance(result, ExecutionErrorResult):
                return result
        return None

    def get_output_similarity_ratio(self, other: "ExecutionCompositeResult"):
        """
        Compare output of two files
        """

        output1 = self.get_content()
        output2 = other.get_content()

        return SequenceMatcher(None, output1, output2).ratio()
