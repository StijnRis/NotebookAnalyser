from abc import ABC, abstractmethod


class CodeOutput(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass


class StreamResult(CodeOutput):
    def __init__(self, name: str, text: str):
        super().__init__()
        self.name = name
        self.text = text

    def to_string(self) -> str:
        return self.text


class ErrorResult(CodeOutput):
    def __init__(self, traceback: list[str], ename: str, evalue: str):
        super().__init__()
        self.traceback = traceback
        self.ename = ename
        self.evalue = evalue

    def to_string(self) -> str:
        return self.evalue


class ExecuteResult(CodeOutput):
    def __init__(self, result: dict):
        super().__init__()
        self.result = result

    def to_string(self) -> str:
        return str(self.result)


class DisplayDataResult(CodeOutput):
    def __init__(self, data: dict):
        super().__init__()
        self.data = data

    def to_string(self) -> str:
        return "DisplayDataResult"
