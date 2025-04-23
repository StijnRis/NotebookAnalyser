from typing import Any, Generic, List, TypeVar

import xlsxwriter

from report.column.column import Column

T = TypeVar("T", bound=List[Column])


class Sheet(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self.columns: dict[str, Column] = {}
        self.number_of_rows = 0

    def add_row(self, row: dict[str, Any]) -> None:
        if len(row) != len(self.columns):
            raise ValueError("Row length does not match number of columns")
        self.number_of_rows += 1
        for column in self.columns.values():
            if column.name not in row:
                raise ValueError(f"Row does not contain value for column {column.name}")
            column.add_item(row[column.name])

    def add_column(self, column: Column) -> None:
        if self.number_of_rows > 0:
            raise ValueError("Cannot add columns after rows have been added")
        if column.name in self.columns:
            raise ValueError(f"Column {column.name} already exists")
        self.columns[column.name] = column
    
    def add_columns(self, columns: list[Column]) -> None:
        if self.number_of_rows > 0:
            raise ValueError("Cannot add columns after rows have been added")
        for column in columns:
            self.add_column(column)

    def write_to_workbook(self, workbook: xlsxwriter.Workbook) -> None:
        # Create the main worksheet
        main_worksheet = workbook.add_worksheet(self.name)

        # Setup header format
        header_format = workbook.add_format()
        header_format.set_bold(True)
        header_format.set_align("center")
        header_format.set_align("vcenter")
        header_format.set_rotation(45)
        header_format.set_text_wrap(True)

        # Write headers
        main_worksheet.set_row(0, 80, header_format)
        keys = [column.name for column in self.columns.values()]
        for i, key in enumerate(keys):
            main_worksheet.write(0, i, key)
        main_worksheet.freeze_panes(1, 0)

        # Format the entire worksheet as a table
        column_settings = [{"header": key} for key in keys]
        main_worksheet.add_table(
            0,
            0,
            self.number_of_rows,
            len(self.columns) - 1,
            {"columns": column_settings, "style": "Table Style Medium 9"},
        )

        for i, column in enumerate(self.columns.values()):
            column.write_to_sheet(workbook, main_worksheet, i)
