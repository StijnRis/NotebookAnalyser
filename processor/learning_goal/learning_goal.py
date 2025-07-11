import ast
from abc import ABC, abstractmethod


class LearningGoal(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def is_applied_in(self, code: ast.AST) -> bool:
        """
        Checks if the learning goal is applied in the code. Does not check childs of the ast node.
        """
        pass

        
    @abstractmethod
    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Checks if code related to the learning goal is in the error.
        """
        pass