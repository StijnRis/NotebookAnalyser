import ast

from processor.learning_goal.learning_goal import LearningGoal


class VariableAssignmentLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Variable assignment", "Assigning values to variables.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, (ast.Assign, ast.AugAssign))

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects variable assignment errors using error name and message.
        """
        if "nameerror" in error_name.lower() and "not defined" in traceback.lower():
            return True
        return False
