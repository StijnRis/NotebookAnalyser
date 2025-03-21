from typing import Any, Dict, List, Optional

from code_log.code.code import Code


class CodeSnippet(Code):
    """
    A code snippet (cell in a notebook).
    """

    @staticmethod
    def load(dict: Dict[str, Any]):
        return CodeSnippet(
            dict.get("id", None),
            dict["cell_type"],
            dict["source"],
            dict["metadata"],
            [NotebookContentOutput.load(x) for x in dict.get("outputs", [])],
            dict.get("execution_count", None),
        )

    def __init__(
        self,
        id: Optional[int],
        cell_type: str,
        source: str,
        metadata: Dict[str, Any],
        execution_count: Optional[int],
    ):
        self.id = id
        self.cell_type = cell_type
        self.source = source
        self.metadata = metadata
        self.outputs = outputs
        self.execution_count = execution_count
    
    def get_source(self):
        return self.source



