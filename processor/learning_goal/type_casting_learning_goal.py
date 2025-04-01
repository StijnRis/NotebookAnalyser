import ast

from processor.learning_goal.learning_goal import LearningGoal


class TypeCastingLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Type casting", "Operation involving data types.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id
                in {"int", "float", "str", "bool", "list", "dict", "set", "tuple"}
            ):
                count += 1
        return count
