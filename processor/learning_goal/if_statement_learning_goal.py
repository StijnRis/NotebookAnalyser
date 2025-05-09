import ast

from processor.learning_goal.learning_goal import LearningGoal


class IfStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__(
            "If statement", "Using if statements to control the flow of the program."
        )

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.If)

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects if statement errors using error name and message.
        """
        return False
