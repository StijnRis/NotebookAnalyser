import ast

from processor.learning_goal.learning_goal import LearningGoal


class WhileLoopLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("While loop", "Error with a while loop.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.While):
                count += 1
        return count
