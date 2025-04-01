import ast

from processor.learning_goal.learning_goal import LearningGoal


class ListAccessLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Accessing list", "Error with accessing a list.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.Subscript):
                count += 1
        return count
