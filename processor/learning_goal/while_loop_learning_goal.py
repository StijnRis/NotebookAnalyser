import ast

from processor.learning_goal.learning_goal import LearningGoal


class WhileLoopLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("While loop", "Error with a while loop.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.While)
