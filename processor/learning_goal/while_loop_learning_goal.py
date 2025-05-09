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

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects while loop errors using error name and traceback.
        """
        if "syntaxerror" in error_name.lower() and "while" in traceback.lower():
            return True
        return False
