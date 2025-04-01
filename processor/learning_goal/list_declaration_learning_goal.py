import ast

from processor.learning_goal.learning_goal import LearningGoal


class ListDeclarationLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Lists declaration", "Error with defining a list.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.List):
                count += 1
        return count
