from enum import Enum
from typing import Any, Optional


class NotebookContentOutputType(Enum):
    STREAM = "stream"
    ERROR = "error"
    EXECUTE_RESULT = "execute_result"
    DISPLAY_DATA = "display_data"


class NotebookContentOutput:
    @staticmethod
    def load(dict: dict[str, Any]):
        output_type = NotebookContentOutputType(dict["output_type"])
        if output_type == NotebookContentOutputType.STREAM:
            return NotebookContentOutput(
                output_type,
                name=dict["name"],
                text=dict["text"],
            )
        elif output_type == NotebookContentOutputType.ERROR:
            return NotebookContentOutput(
                output_type,
                traceback=dict["traceback"],
                ename=dict["ename"],
                evalue=dict["evalue"],
            )
        elif output_type == NotebookContentOutputType.EXECUTE_RESULT:
            return NotebookContentOutput(
                output_type
            )
        elif output_type == NotebookContentOutputType.DISPLAY_DATA:
            return NotebookContentOutput(
                output_type
            )
        else:
            raise ValueError(f"Unknown output type: {dict['output_type']}")

    def __init__(
        self,
        output_type: NotebookContentOutputType,
        name: Optional[str] = None,
        text: Optional[str] = None,
        traceback: Optional[list[str]] = None,
        ename: Optional[str] = None,
        evalue: Optional[str] = None,
    ):
        self.output_type = output_type
        self.name = name
        self.text = text
        self.traceback = traceback
        self.ename = ename
        self.evalue = evalue
