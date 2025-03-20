from datetime import datetime, timedelta
from enum import Enum
from typing import List, Sequence

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from content_log.progression.notebook_progression_with_datetime import (
    NotebookProgressionWithDatetime,
)
from content_log.progression.time_series import TimeSeries


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
            elif isinstance(data[0][key], TimeSeries):
                self.write_column_with_timeseries_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], NotebookProgressionWithDatetime):
                self.write_column_with_notebook_progression_with_datetime_data(
                    worksheet, keys.index(key), key, column_data
                )
            elif isinstance(data[0][key], Enum):
                self.write_column_with_enum_data(
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

    def write_column_with_timeseries_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: Sequence[TimeSeries],
    ):
        # Create the worksheets for keys with multiple values
        worksheet_name = worksheet.name
        x_name = f"y {worksheet_name} - {column_name}"[:31]
        Y_name = f"x {worksheet_name} - {column_name}"[:31]
        worksheet_x = self.workbook.add_worksheet(x_name)
        worksheet_x.hide()
        worksheet_y = self.workbook.add_worksheet(Y_name)
        worksheet_y.hide()

        # Save data
        for i, item in enumerate(column_data):
            worksheet_x.write_row(i + 1, column_nr, item.times)
            worksheet_y.write_row(i + 1, column_nr, item.data)
            end_column = xl_col_to_name(len(item.times))
            negative_value = any(value < 0 for value in item.data)
            worksheet.add_sparkline(
                i + 1,
                column_nr,
                {
                    "range": f"'{worksheet_y.name}'!$A${i + 2}:${end_column}${i + 2}",
                    "date_axis": f"'{worksheet_x.name}'!$A${i + 2}:${end_column}${i + 2}",
                    "type": "line",
                    "axis": negative_value,
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
        time_format_normal = self.workbook.add_format({"num_format": '[hh]:mm"h"'})
        time_format_seconds = self.workbook.add_format({"num_format": '[s]"s"'})
        for i, item in enumerate(column_data):
            total_seconds = item.total_seconds()
            if total_seconds < 60:
                worksheet.write(i + 1, column_nr, item, time_format_seconds)
            else:
                worksheet.write(i + 1, column_nr, item, time_format_normal)

    def write_column_with_notebook_progression_with_datetime_data(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
        column_name: str,
        column_data: list[NotebookProgressionWithDatetime],
    ):
        # Convert NotebookProgression to TimeSeries
        timeseries_data = [item.convert_to_notebook_progression() for item in column_data]
        self.write_column_with_timeseries_data(
            worksheet, column_nr, column_name, timeseries_data
        )

    def close(self):
        while True:
            try:
                self.workbook.close()
                break
            except Exception as e:
                print(f"Error encountered: {e}.")
                input("Close notebook so it can be saved.")
                self.close()
