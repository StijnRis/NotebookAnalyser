import xlsxwriter

from report.column.column import Column


class MultilineTextColumn(Column[str]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[str] = []

    def add_item(self, item: str):
        if not isinstance(item, str):
            raise TypeError(f"Item must be of type str, got {type(item).__name__}")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        cell_format = workbook.add_format({'text_wrap': True})
        worksheet.set_column(column_nr, column_nr, 48, cell_format)  # Convert pixels to Excel column width
        for row, item in enumerate(self.items, start=1):
            worksheet.write(row, column_nr, item)
