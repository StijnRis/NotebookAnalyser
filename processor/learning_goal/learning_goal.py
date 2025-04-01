from abc import ABC, abstractmethod
import ast


class LearningGoal(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def count_applications_in(self, code: ast.AST) -> int:
        """
        Count how many times the learning goal is applied in the code
        """
        pass
