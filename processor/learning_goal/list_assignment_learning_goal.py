import ast

from processor.learning_goal.learning_goal import LearningGoal


class ListAssignmentLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Setting list", "Error with setting a value in a list.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.Assign) and isinstance(
            code.targets[0], ast.Subscript
        )

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects list assignment errors using error name and message.
        """
        error_name_l = error_name.lower()
        if "indexerror" in error_name_l:
            return True
        if (
            "typeerror" in error_name_l
            and "object is not subscriptable" in error_name_l
        ):
            return True
        if "keyerror" in error_name_l:
            return True
        return False
