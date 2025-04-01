import ast

from processor.learning_goal.learning_goal import LearningGoal


class ImportStatementLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__("Import statement", "Error with an import statement.")

    def count_applications_in(self, code: ast.AST) -> int:
        count = 0
        for node in ast.walk(code):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                count += 1
        return count
