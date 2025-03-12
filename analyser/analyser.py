from abc import ABC, abstractmethod
from typing import Any
from report.report_generator import ReportGenerator
from user.user import User

class Analyser(ABC):
    def __init__(self):
        self.data: list[dict[str, Any]] = []

    @abstractmethod
    def analyse_user(self, user: User):
        pass

    def preprocess_data(self):
        """Called before saving results"""
        pass

    def save_result_to_report(self, report: ReportGenerator):
        self.preprocess_data()
        report.display_data(f"{self.__class__.__name__}", self.data)