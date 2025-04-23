from datetime import datetime

import xlsxwriter

from report.column.column import Column


class DatetimeColumn(Column[datetime]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[datetime] = []

    def add_item(self, item: datetime):
        if not isinstance(item, datetime):
            raise TypeError(f"Item must be of type datetime, got {type(item).__name__}")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        date_format = workbook.add_format({"num_format": "dd/mm/yy hh:mm"})
        worksheet.set_column(column_nr, column_nr, 13)
        for row, item in enumerate(self.items, start=1):
            worksheet.write(row, column_nr, item, date_format)
