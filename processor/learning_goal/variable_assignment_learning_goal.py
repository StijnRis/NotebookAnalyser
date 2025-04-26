import ast

from processor.learning_goal.learning_goal import LearningGoal


class VariableAssignmentLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Variable assignment", "Assigning values to variables.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, (ast.Assign, ast.AugAssign))