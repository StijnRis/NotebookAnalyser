from enum import Enum

import xlsxwriter

from report.column.column import Column


class EnumColumn(Column[Enum]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[Enum] = []

    def add_item(self, item: Enum):
        if not isinstance(item, Enum):
            raise TypeError(f"Item must be of type Enum, got {type(item).__name__}")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        for row, item in enumerate(self.items, start=1):
            worksheet.write(row, column_nr, item.name)

        worksheet.set_column(column_nr, column_nr, 15)
        enum_class = type(self.items[0])
        enum_values = [e.name for e in enum_class.__members__.values()]
        worksheet.data_validation(
            1,
            column_nr,
            len(self.items),
            column_nr,
            {"validate": "list", "source": enum_values},
        )
