import ast
from datetime import datetime
from difflib import SequenceMatcher


class SourceCode:
    def __init__(self, time: datetime, code: str):
        self.code = code
        self.time = time

    def get_time(self) -> datetime:
        return self.time

    def get_code(self) -> str:
        return self.code

    def get_ast(self) -> ast.Module:
        try:
            return ast.parse(self.get_code())
        except SyntaxError:
            return ast.Module(body=[], type_ignores=[])

    # TODO compare by amount of operation needed on the three to make them similar
    def get_ast_difference_ratio(self, other: "SourceCode"):
        """
        Compare ast trees of two notebooks
        """

        ast1 = ast.dump(self.get_ast())
        ast2 = ast.dump(other.get_ast())

        similarity = SequenceMatcher(None, ast1, ast2).ratio()

        return similarity

    def get_code_difference_ratio(self, other: "SourceCode"):
        """
        Compare output of two notebooks
        """

        output1 = self.get_code()
        output2 = other.get_code()

        return SequenceMatcher(None, output1, output2).ratio()
