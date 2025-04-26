import ast
from datetime import datetime
from difflib import SequenceMatcher, ndiff, unified_diff


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

    def get_ast_of_lines(self, lines: list[int]) -> list[ast.AST]:
        body = []
        parsed_ast = self.get_ast()
        for node in ast.walk(parsed_ast):
            if (
                hasattr(node, "lineno")
                and node.lineno in lines
            ):
                body.append(node)
        return body

    def get_code_difference_ratio(self, other: "SourceCode") -> float:
        """
        Compare output of two notebooks
        """

        output1 = self.get_code()
        output2 = other.get_code()

        return SequenceMatcher(None, output1, output2).ratio()

    def get_code_difference(self, other: "SourceCode") -> str:
        """
        Compare code of two files
        """

        differences = "\n".join(
            unified_diff(
                other.get_code().splitlines(),
                self.get_code().splitlines(),
                lineterm="",
            )
        )
        return differences

    def get_line_numbers_of_new_code(self, original: "SourceCode") -> list[int]:
        """
        Returns the lines numbers of the lines that were added in this file
        """
        diff = ndiff(original.get_code().splitlines(), self.get_code().splitlines())

        original_line = 0
        new_line = 0
        changes: list[int] = []

        for line in diff:
            code = line[:2]
            content = line[2:]

            if code == "  ":  # Unchanged line
                original_line += 1
                new_line += 1
            elif code == "- ":  # Line removed from original
                original_line += 1
            elif code == "+ ":  # Line added in new file
                changes.append(new_line + 1)
                new_line += 1

        return changes

    def get_asts_of_new_code(self, original: "SourceCode") -> list[ast.AST]:
        """
        Returns the AST of the lines that were added in this file
        """
        lines = self.get_line_numbers_of_new_code(original)
        return self.get_ast_of_lines(lines)
    
    
