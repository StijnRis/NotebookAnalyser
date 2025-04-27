from datetime import datetime, timedelta

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

        # Calculate offset
        first_datetime = datetime(2100, 1, 1)
        last_datetime = datetime(1970, 1, 1)
        for item_list in self.items:
            for item in item_list:
                first_datetime = min(first_datetime, item[0])
                last_datetime = max(last_datetime, item[1])

        duration = last_datetime - first_datetime
        scale = 1
        if duration > timedelta(days=1):
            scale = 1 / timedelta(days=1).total_seconds()
        elif duration > timedelta(hours=1):
            scale = 1 / timedelta(hours=1).total_seconds()
        elif duration > timedelta(minutes=1):
            scale = 1 / timedelta(minutes=1).total_seconds()

        # Save data
        for row, item_list in enumerate(self.items):
            # Make all start at same moment
            worksheet_x.write(row + 1, 0, 0)
            worksheet_y.write(row + 1, 0, 0)

            for column, item in enumerate(item_list):
                first = (item[0] - first_datetime).total_seconds() * scale
                last = (item[1] - first_datetime).total_seconds() * scale
                worksheet_x.write(row + 1, 4 * column + 1, first)
                worksheet_y.write(row + 1, 4 * column + 1, 0)
                worksheet_x.write(row + 1, 4 * column + 2, first)
                worksheet_y.write(row + 1, 4 * column + 2, 1)
                worksheet_x.write(row + 1, 4 * column + 3, last)
                worksheet_y.write(row + 1, 4 * column + 3, 1)
                worksheet_x.write(row + 1, 4 * column + 4, last)
                worksheet_y.write(row + 1, 4 * column + 4, 0)

            # Make all end at same moment
            worksheet_x.write(
                row + 1, len(item_list) * 4 + 1, (last_datetime - first_datetime).total_seconds() * scale
            )
            worksheet_y.write(row + 1, len(item_list) * 4 + 1, 0)

            end_column = xl_col_to_name(len(item_list) * 4 + 1)
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
