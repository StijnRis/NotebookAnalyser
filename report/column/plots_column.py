from typing import List, Tuple

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from report.column.column import Column
from report.report_generator import shorten_string


class PlotsColumn(Column[List[Tuple[float, float]]]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: List[List[Tuple[float, float]]] = []

    def add_item(self, item: List[Tuple[float, float]]):
        if not isinstance(item, list) or not all(
            isinstance(t, tuple)
            and len(t) == 2
            and all(isinstance(x, float) for x in t)
            for t in item
        ):
            raise TypeError("Item must be a list of 2-tuples with floats")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        worksheet_name = worksheet.name
        x_name = shorten_string(f"x {worksheet_name} - {self.name}", 31)
        y_name = shorten_string(f"y {worksheet_name} - {self.name}", 31)
        worksheet_x = workbook.add_worksheet(x_name)
        worksheet_x.hide()
        worksheet_y = workbook.add_worksheet(y_name)
        worksheet_y.hide()

        # Save data
        for row, item_list in enumerate(self.items):
            for column, item in enumerate(item_list):
                worksheet_x.write(row + 1, column, item[0])
                worksheet_y.write(row + 1, column, item[1])
            end_column = xl_col_to_name(len(item_list))
            worksheet.add_sparkline(
                row + 1,
                column_nr,
                {
                    "range": f"'{worksheet_y.name}'!$A${row + 2}:${end_column}${row + 2}",
                    "date_axis": f"'{worksheet_x.name}'!$A${row + 2}:${end_column}${row + 2}",
                    "type": "line",
                },
            )

        # Apply format to multi-valued columns
        worksheet.set_column(column_nr, column_nr, 20)
