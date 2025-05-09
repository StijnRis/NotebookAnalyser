import ast

from processor.learning_goal.learning_goal import LearningGoal


class TypeCastingLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Type casting", "Operation involving data types.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return (
            isinstance(code, ast.Call)
            and isinstance(code.func, ast.Name)
            and code.func.id
            in {"int", "float", "str", "bool", "list", "dict", "set", "tuple"}
        )

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects type casting errors using error name and message.
        """
        if (
            "typeerror" in error_name.lower()
        ):
            return True
        return False
