# import ast
# from difflib import SequenceMatcher
# from typing import Any, Dict, List

# from content_log.notebook_content.notebook_content_cell import NotebookContentCell
# from content_log.notebook_content.notebook_content_output import NotebookContentOutputType


# class NotebookContent:
#     @staticmethod
#     def load(dict: dict[str, Any]):
#         return NotebookContent(
#             dict["metadata"],
#             dict["nbformat"],
#             dict["nbformat_minor"],
#             [NotebookContentCell.load(cell) for cell in dict["cells"]],
#         )

#     def __init__(
#         self,
#         metadata: Dict[str, Any],
#         nbformat: int,
#         nbformat_minor: int,
#         cells: List[NotebookContentCell],
#     ):
#         self.metadata = metadata
#         self.nbformat = nbformat
#         self.nbformat_minor = nbformat_minor
#         self.cells = cells
    
#     def get_cell_by_id(self, id: int):
#         for cell in self.cells:
#             if cell.id == id:
#                 return cell
#         return None

#     def get_source_as_string(self):
#         """
#         Get the content of the notebook as a string.
#         """
#         return "\n\n".join([cell.source for cell in self.cells])

#     def get_code_as_string(self):
#         """
#         Get all the code of the notebook as a string.
#         """
#         code_cells = []
#         for cell in self.cells:
#             if cell.cell_type == "code":
#                 code_cells.append(cell)
#         return "\n\n".join([cell.source for cell in code_cells])

#     def get_outputs(self):
#         """
#         Get the outputs of the notebook.
#         """
#         outputs: list[str] = []
#         for cell in self.cells:
#             if cell.cell_type != "code":
#                 continue

#             # Add output of cell
#             total_output = ""
#             for output in cell.outputs:
#                 output_type = output.output_type
#                 if output_type == NotebookContentOutputType.STREAM:
#                     total_output += str(output.text)
#                 elif output_type == NotebookContentOutputType.ERROR:
#                     total_output += str(output.ename)
#                 elif output_type == NotebookContentOutputType.EXECUTE_RESULT:
#                     pass
#                 elif output_type == NotebookContentOutputType.DISPLAY_DATA:
#                     pass
#                 else:
#                     raise ValueError(f"Unknown output type: {output_type}")
#             outputs.append(total_output)

#         return outputs

#     def get_ast(self):
#         content = self.get_code_as_string()
#         try:
#             return ast.parse(content)
#         except SyntaxError:
#             return ast.Module(body=[], type_ignores=[])

#     # TODO compare by amount of operation needed on the three to make them similar
#     def get_ast_difference_ratio(self, other: "NotebookContent"):
#         """
#         Compare ast trees of two notebooks
#         """

#         ast1 = ast.dump(self.get_ast())
#         ast2 = ast.dump(other.get_ast())

#         similarity = SequenceMatcher(None, ast1, ast2).ratio()

#         return similarity

#     def get_output_difference_ratio(self, other: "NotebookContent"):
#         """
#         Compare output of two notebooks
#         """

#         output1 = self.get_outputs()
#         output2 = other.get_outputs()

#         return SequenceMatcher(None, output1, output2).ratio()
    
#     def get_code_difference_ratio(self, other: "NotebookContent"):
#         """
#         Compare output of two notebooks
#         """

#         output1 = self.get_code_as_string()
#         output2 = other.get_code_as_string()

#         return SequenceMatcher(None, output1, output2).ratio()
