import ast

from processor.learning_goal.learning_goal import LearningGoal


class FunctionCallLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Function call", "Error with a function call.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.Call)
