import ast

from processor.learning_goal.learning_goal import LearningGoal


class ForLoopLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("For loop", "Error with a for loop.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.For):
                count += 1
        return count
