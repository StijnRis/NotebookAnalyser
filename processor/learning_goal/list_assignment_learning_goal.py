import ast

from processor.learning_goal.learning_goal import LearningGoal


class ListAssignmentLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Setting list", "Error with setting a value in a list.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.Assign) and isinstance(
                node.targets[0], ast.Subscript
            ):
                count += 1
        return count
