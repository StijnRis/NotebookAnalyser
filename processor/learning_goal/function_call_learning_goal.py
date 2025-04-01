import ast

from processor.learning_goal.learning_goal import LearningGoal


class FunctionCallLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Function call", "Error with a function call.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.Call):
                count += 1
        return count
