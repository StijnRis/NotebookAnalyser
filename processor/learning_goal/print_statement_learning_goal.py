import ast

from processor.learning_goal.learning_goal import LearningGoal


class PrintStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Print statement", "Using the print statement.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
            ):
                count += 1
        return count
