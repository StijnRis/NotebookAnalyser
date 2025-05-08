import xlsxwriter

from report.column.column import Column


class BooleanColumn(Column[bool]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[bool] = []

    def add_item(self, item: bool):
        if not isinstance(item, bool):
            raise TypeError(f"Item must be of type str, got {type(item).__name__}")
        self.items.append(item)

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):
        worksheet.set_column(column_nr, column_nr, 1.5)
        green_format = workbook.add_format()
        green_format.set_bg_color('green')
        red_format = workbook.add_format()
        red_format.set_bg_color('red')
        for row, item in enumerate(self.items, start=1):
            if item:
                worksheet.write(row, column_nr, 1, green_format)
            else:
                worksheet.write(row, column_nr, 0, red_format)
            
