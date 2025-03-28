from abc import ABC, abstractmethod
from datetime import datetime
from difflib import SequenceMatcher


class ExecutionOutput(ABC):
    def __init__(self, time: datetime):
        self.time = time

    def get_time(self) -> datetime:
        return self.time

    @abstractmethod
    def get_content(self) -> str:
        pass

    def get_output_similarity_ratio(self, other: "ExecutionOutput"):
        """
        Compare output of two notebooks
        """

        output1 = self.get_content()
        output2 = other.get_content()

        return SequenceMatcher(None, output1, output2).ratio()


class EmptyResult(ExecutionOutput):
    def __init__(self, time: datetime):
        super().__init__(time)

    def get_content(self) -> str:
        return "<EmptyResult>"


class StreamResult(ExecutionOutput):
    """
    "output_type": "stream"
    """

    def __init__(self, time: datetime, content: str):
        super().__init__(time)
        self.content = content

    def get_content(self) -> str:
        return self.content


class ErrorResult(ExecutionOutput):
    def __init__(
        self, time: datetime, traceback: str, error_name: str, error_value: str
    ):
        super().__init__(time)
        self.traceback = traceback
        self.error_name = error_name
        self.error_value = error_value

    def get_traceback(self) -> str:
        return self.traceback

    def get_error_name(self) -> str:
        return self.error_name

    def get_error_value(self) -> str:
        return self.error_value

    def get_content(self) -> str:
        return f"{self.error_name}: {self.error_value}"


class ExecuteResult(ExecutionOutput):
    def __init__(self, time: datetime, result: dict):
        super().__init__(time)
        self.result = result

    def get_content(self) -> str:
        return str(self.result)


class DisplayDataResult(ExecutionOutput):
    def __init__(self, time: datetime, data: dict):
        super().__init__(time)
        self.data = data

    def get_content(self) -> str:
        return "DisplayDataResult"
