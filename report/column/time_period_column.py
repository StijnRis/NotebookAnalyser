from datetime import datetime

from xlsxwriter.utility import xl_col_to_name

from report.column.column import Column
from report.report_generator import shorten_string


class TimePeriodColumn(Column[list[tuple[datetime, datetime]]]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[list[tuple[datetime, datetime]]] = []

    def add_item(self, item: list[tuple[datetime, datetime]]):
        if not isinstance(item, list) or not all(
            isinstance(t, tuple) and len(t) == 2 for t in item
        ):
            raise TypeError("Item must be a list of 2-tuples")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook,
        worksheet,
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
            offset = (
                min([min(item) for item in item_list])
                if (len(item_list) > 0)
                else datetime.fromtimestamp(0)
            )
            for column, item in enumerate(item_list):
                start = (item[0] - offset).total_seconds()
                end = (item[1] - offset).total_seconds()
                worksheet_x.write(row + 1, 4 * column, start)
                worksheet_y.write(row + 1, 4 * column, 0)
                worksheet_x.write(row + 1, 4 * column + 1, start)
                worksheet_y.write(row + 1, 4 * column + 1, 1)
                worksheet_x.write(row + 1, 4 * column + 2, end)
                worksheet_y.write(row + 1, 4 * column + 2, 1)
                worksheet_x.write(row + 1, 4 * column + 3, end)
                worksheet_y.write(row + 1, 4 * column + 3, 0)
            end_column = xl_col_to_name(len(item_list) * 4)
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
