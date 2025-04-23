from datetime import timedelta

import xlsxwriter

from report.column.column import Column


class TimedeltaColumn(Column[timedelta]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[timedelta] = []

    def add_item(self, item: timedelta):
        if not isinstance(item, timedelta):
            raise TypeError(
                f"Item must be of type timedelta, got {type(item).__name__}"
            )
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        time_format_seconds = workbook.add_format({"num_format": '[s]"s"'})
        time_format_minutes = workbook.add_format({"num_format": '[m]"m"'})
        time_format_hours = workbook.add_format({"num_format": '[h]"h"'})
        for i, item in enumerate(self.items):
            total_seconds = item.total_seconds()
            if total_seconds < 60:
                worksheet.write(i + 1, column_nr, item, time_format_seconds)
            elif total_seconds < 3600:
                worksheet.write(i + 1, column_nr, item, time_format_minutes)
            else:
                worksheet.write(i + 1, column_nr, item, time_format_hours)
