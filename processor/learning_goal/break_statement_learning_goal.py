import ast

from processor.learning_goal.learning_goal import LearningGoal


class BreakStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Break statement", "Error with a break statement.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.Break)

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects break statement errors using error name and traceback, similar to mapping strategy.
        """
        if "syntaxerror" in error_name.lower() and "break" in traceback.lower():
            return True
        return False
