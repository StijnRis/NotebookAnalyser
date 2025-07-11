import ast
from datetime import datetime
from difflib import SequenceMatcher, ndiff, unified_diff

from event_log.event import Event
from processor.learning_goal.learning_goal import LearningGoal


class SourceCode(Event):
    def __init__(self, time: datetime, code: str):
        self.code = code
        self.time = time

    def get_time(self) -> datetime:
        return self.time

    def get_code(self) -> str:
        return self.code

    def get_ast(self) -> ast.Module:
        try:
            return ast.parse(self.code)
        except SyntaxError:
            return ast.Module(body=[], type_ignores=[])

    def get_ast_of_lines(self, lines: list[int]) -> list[ast.AST]:
        body = []
        parsed_ast = self.get_ast()
        for node in ast.walk(parsed_ast):
            if hasattr(node, "lineno") and node.lineno in lines:
                body.append(node)
        return body

    def get_code_difference_ratio(self, other: "SourceCode") -> float:
        """
        Compare output of two files
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

    def get_line_numbers_of_added_code(self, new_code: "SourceCode") -> list[int]:
        """
        Returns the lines numbers of the lines that were added in the other file
        """
        diff = ndiff(self.get_code().splitlines(), new_code.get_code().splitlines())

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

    def get_added_ast_items(self, new_code: "SourceCode") -> list[ast.AST]:
        """
        Returns the AST of the lines that were added in the other file
        """
        lines = self.get_line_numbers_of_added_code(new_code)
        return new_code.get_ast_of_lines(lines)

    def get_learning_goals_applied_on_lines(
        self, lines: list[int], learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        """
        Get the learning goals applied between two datetime points.
        """
        ast_items = self.get_ast_of_lines(lines)

        learning_goals_in_ast = []
        for ast_item in ast_items:
            for goal in learning_goals:
                if goal.is_applied_in(ast_item):
                    learning_goals_in_ast.append(goal)

        return learning_goals_in_ast
