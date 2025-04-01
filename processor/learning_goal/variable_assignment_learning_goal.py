import ast
from processor.learning_goal.learning_goal import LearningGoal


class VariableAssignmentLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Variable assignment", "Assigning values to variables.")

    def count_applications_in(self, code: ast.AST) -> int:
        """
        Count how many times a variable assignment is used in the code
        """
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.Assign):
                count += 1
        return count