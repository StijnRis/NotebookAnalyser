from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import xlsxwriter

T = TypeVar("T")


class Column(ABC, Generic[T]):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def add_item(self, item: T):
        pass

    @abstractmethod
    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        pass

def shorten_string(string: str, length: int):
    new_string = ""
    pos = 0
    string_length = len(string)
    while pos < len(string):
        new_string += string[pos]
        pos += max(1, (string_length - pos) // (length - len(new_string)))
    return new_string