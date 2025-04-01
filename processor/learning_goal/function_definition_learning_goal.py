import ast

from processor.learning_goal.learning_goal import LearningGoal


class FunctionDefinitionLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Function definition", "Error with a function definition.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.FunctionDef):
                count += 1
        return count
