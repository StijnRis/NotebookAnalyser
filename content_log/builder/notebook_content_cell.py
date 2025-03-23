# from typing import Any, Dict, List, Optional

# from content_log.notebook_content.notebook_content_output import NotebookContentOutput


# class NotebookContentCell:
#     """
#     A cell in a notebook.
#     """

#     @staticmethod
#     def load(dict: Dict[str, Any]):
#         return NotebookContentCell(
#             dict.get("id", None),
#             dict["cell_type"],
#             dict["source"],
#             dict["metadata"],
#             [NotebookContentOutput.load(x) for x in dict.get("outputs", [])],
#             dict.get("execution_count", None),
#         )

#     def __init__(
#         self,
#         id: Optional[int],
#         cell_type: str,
#         source: str,
#         metadata: Dict[str, Any],
#         outputs: List[NotebookContentOutput],
#         execution_count: Optional[int],
#     ):
#         self.id = id
#         self.cell_type = cell_type
#         self.source = source
#         self.metadata = metadata
#         self.outputs = outputs
#         self.execution_count = execution_count

#     def get_source(self):
#         return self.source
