from abc import ABC, abstractmethod
from typing import Any

from report.report_generator import ReportGenerator
from report.sheet import Sheet
from user.user import User


class Analyser(ABC):
    def __init__(self):
        self.sheet = Sheet(self.__class__.__name__)

    @abstractmethod
    def analyse_user(self, user: User):
        pass

    def preprocess_data(self):
        """Called before saving results"""
        pass

    def save_result_to_report(self, report: ReportGenerator):
        self.preprocess_data()
        report.display_sheet(self.sheet)
