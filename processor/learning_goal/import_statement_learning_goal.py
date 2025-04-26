import ast

from processor.learning_goal.learning_goal import LearningGoal


class ImportStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Import statement", "Error with an import statement.")

    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        return isinstance(code, ast.Import) or isinstance(code, ast.ImportFrom)
