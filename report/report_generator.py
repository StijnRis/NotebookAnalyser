from datetime import datetime, timedelta
from enum import Enum
from typing import Sequence

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name


def is_list_of_tuple_float_float(data):
    return isinstance(data, list) and all(
        isinstance(item, tuple)
        and len(item) == 2
        and (isinstance(item[0], float) or isinstance(item[1], float))
        for item in data
    )


def is_list_of_tuple_float_bool(data):
    return isinstance(data, list) and all(
        isinstance(item, tuple)
        and len(item) == 2
        and (isinstance(item[0], float) or isinstance(item[1], bool))
        for item in data
    )

def is_list_of_tuple_datetime_datetime(data):
    return isinstance(data, list) and all(
        isinstance(item, tuple)
        and len(item) == 2
        and (isinstance(item[0], datetime) or isinstance(item[1], datetime))
        for item in data
    )


class ReportGenerator:
    def __init__(self, file_path: str):
        self.workbook = xlsxwriter.Workbook(file_path, {"nan_inf_to_errors": True})

    def display_data(self, worksheet_name: str, data: list[dict]):
        # Check that all have same keys
        keys = list(data[0].keys())
        for item in data:
            assert keys == list(item.keys()), "All items must have the same keys"

        # Create the main worksheet
        main_worksheet = self.workbook.add_worksheet(worksheet_name)

        # Setup header format
        header_format = self.workbook.add_format()
        header_format.set_bold(True)
        header_format.set_align("center")
        header_format.set_align("vcenter")
        header_format.set_rotation(45)

        # Write headers
        main_worksheet.set_row(0, 80, header_format)
        for i, key in enumerate(keys):
            main_worksheet.write(0, i, key)
        main_worksheet.freeze_panes(1, 0)

        # Format the entire worksheet as a table
        column_settings = [{"header": key} for key in keys]
        main_worksheet.add_table(
            0,
            0,
            len(data),
            len(keys) - 1,
            {"columns": column_settings, "style": "Table Style Medium 9"},
        )

        # Write data
        self.write_columns(main_worksheet, data)

    def write_columns(
        self, worksheet: xlsxwriter.Workbook.worksheet_class, data: list[dict]
    ):
        keys = list(data[0].keys())
        for key in keys:
            column_data = [item[key] for item in data]
            if isinstance(data[0][key], (int, float)):
                self.write_column_with_numeric_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], str):
                self.write_column_with_text_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], datetime):
                self.write_column_with_datetime_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], timedelta):
                self.write_column_with_timedelta_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif is_list_of_tuple_float_float(data[0][key]):
                self.write_column_with_list_of_tuple_float_float(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], Enum):
                self.write_column_with_enum_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif is_list_of_tuple_float_bool(data[0][key]):
                self.write_column_with_list_of_tuple_float_bool(
                    worksheet, keys.index(key), key, column_data
                )
            elif is_list_of_tuple_datetime_datetime(data[0][key]):
                self.write_column_with_list_of_tuple_datetime_datetime(
                    worksheet, keys.index(key), key, column_data
                )
            else:
                raise ValueError(f"Unsupported type: {type(data[0][key])}")

    def write_column_with_text_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[str],
    ):
        for i, item in enumerate(column_data):
            worksheet.write(i + 1, column_nr, item)

    def write_column_with_list_of_tuple_float_float(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[list[tuple[float, float]]],
    ):
        # Create the worksheets for keys with multiple values
        worksheet_name = worksheet.name
        x_name = f"x {worksheet_name} - {column_name}"[:31]
        Y_name = f"y {worksheet_name} - {column_name}"[:31]
        worksheet_x = self.workbook.add_worksheet()
        worksheet_x.hide()
        worksheet_y = self.workbook.add_worksheet()
        worksheet_y.hide()

        # Save data
        for row, item_list in enumerate(column_data):
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
    
    def write_column_with_list_of_tuple_float_bool(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[list[tuple[float, bool]]],
    ):
        # Create the worksheets for keys with multiple values
        worksheet_name = worksheet.name
        x_name = f"x {worksheet_name} - {column_name}"[:31]
        Y_name = f"y {worksheet_name} - {column_name}"[:31]
        worksheet_x = self.workbook.add_worksheet()
        worksheet_x.hide()
        worksheet_y = self.workbook.add_worksheet()
        worksheet_y.hide()

        # Save data
        for row, item_list in enumerate(column_data):
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
                    "type": "column",
                    "style": 5,
                },
            )

        # Apply format to multi-valued columns
        worksheet.set_column(column_nr, column_nr, 20)
    
    def write_column_with_list_of_tuple_datetime_datetime(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[list[tuple[datetime, datetime]]],
    ):
        # Create the worksheets for keys with multiple values
        worksheet_name = worksheet.name
        x_name = f"x {worksheet_name} - {column_name}"[:31]
        Y_name = f"y {worksheet_name} - {column_name}"[:31]
        worksheet_x = self.workbook.add_worksheet()
        worksheet_x.hide()
        worksheet_y = self.workbook.add_worksheet()
        worksheet_y.hide()

        # Save data
        for row, item_list in enumerate(column_data):
            offset = min([min(item) for item in item_list]) if (len(item_list) > 0) else datetime.fromtimestamp(0)
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

    def write_column_with_numeric_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[int | float],
    ):
        for i, item in enumerate(column_data):
            worksheet.write(i + 1, column_nr, item)

        # Apply colour scales to numeric columns
        worksheet.conditional_format(
            1,
            column_nr,
            len(column_data),
            column_nr,
            {
                "type": "3_color_scale",
                "min_type": "num",
                "mid_type": "num",
                "max_type": "num",
            },
        )

    def write_column_with_enum_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[Enum],
    ):
        for i, item in enumerate(column_data):
            worksheet.write(i + 1, column_nr, item.name)

        # Style the column
        worksheet.set_column(column_nr, column_nr, 15)
        enum_class = type(column_data[0])
        enum_values = [e.name for e in enum_class.__members__.values()]
        worksheet.data_validation(
            0,
            column_nr,
            len(column_data),
            column_nr,
            {"validate": "list", "source": enum_values},
        )

    def write_column_with_datetime_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[datetime],
    ):
        date_format = self.workbook.add_format({"num_format": "dd/mm/yy hh:mm"})
        for i, item in enumerate(column_data):
            worksheet.write(i + 1, column_nr, item, date_format)
        worksheet.set_column(column_nr, column_nr, 13)

    def write_column_with_timedelta_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[timedelta],
    ):
        time_format_seconds = self.workbook.add_format({"num_format": '[s]"s"'})
        time_format_minutes = self.workbook.add_format({"num_format": '[m]"m"'})
        time_format_hours = self.workbook.add_format({"num_format": '[h]"h"'})
        for i, item in enumerate(column_data):
            total_seconds = item.total_seconds()
            if total_seconds < 60:
                worksheet.write(i + 1, column_nr, item, time_format_seconds)
            elif total_seconds < 3600:
                worksheet.write(i + 1, column_nr, item, time_format_minutes)
            else:
                worksheet.write(i + 1, column_nr, item, time_format_hours)

    def close(self):
        while True:
            try:
                self.workbook.close()
                break
            except Exception as e:
                print(f"Error encountered: {e}.")
                input("Close notebook so it can be saved.")
                self.close()
