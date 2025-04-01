import ast
from processor.learning_goal.learning_goal import LearningGoal

class IfStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("If statement", "Using if statements to control the flow of the program.")

    def count_applications_in(self, code: ast.AST) -> int:
        """
        Count how many times an if statement is used in the code
        """
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.If):
                count += 1
        return count