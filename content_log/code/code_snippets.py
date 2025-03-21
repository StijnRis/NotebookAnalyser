import ast
from difflib import SequenceMatcher
from typing import Any, Dict, List

from code_log.code.code import Code
from code_log.code.code_snippet import CodeSnippet


class CodeSnippets:
    @staticmethod
    def load(dict: dict[str, Any]):
        return CodeSnippets(
            dict["metadata"],
            dict["nbformat"],
            dict["nbformat_minor"],
            [NotebookContentCell.load(cell) for cell in dict["cells"]],
        )

    def __init__(
        self,
        code_snippets: List[CodeSnippet],
    ):
        self.code_snippets = code_snippets
    
    def get_cell_by_id(self, id: int):
        for cell in self.code_snippets:
            if cell.id == id:
                return cell
        return None

    def get_code_as_string(self):
        """
        Get all the code of the notebook as a string.
        """
        return "\n\n".join([cell.get_source() for cell in self.code_snippets])

    def get_ast(self):
        content = self.get_code_as_string()
        try:
            return ast.parse(content)
        except SyntaxError:
            return ast.Module(body=[], type_ignores=[])

    # TODO compare by amount of operation needed on the three to make them similar
    def get_ast_difference_ratio(self, other: "CodeSnippets"):
        """
        Compare ast trees of two notebooks
        """

        ast1 = ast.dump(self.get_ast())
        ast2 = ast.dump(other.get_ast())

        similarity = SequenceMatcher(None, ast1, ast2).ratio()

        return similarity
    
    def get_code_difference_ratio(self, other: "CodeSnippets"):
        """
        Compare output of two notebooks
        """

        output1 = self.get_code_as_string()
        output2 = other.get_code_as_string()

        return SequenceMatcher(None, output1, output2).ratio()
