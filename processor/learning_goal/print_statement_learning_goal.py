import ast

from processor.learning_goal.learning_goal import LearningGoal


class PrintStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Print statement", "Using the print statement.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return (
            isinstance(code, ast.Call)
            and isinstance(code.func, ast.Name)
            and code.func.id == "print"
        )

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects print statement errors using error name and traceback.
        """
        if "syntaxerror" in error_name.lower() and "print" in traceback.lower():
            return True
        return False
