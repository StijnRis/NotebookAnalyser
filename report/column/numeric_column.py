import xlsxwriter

from report.column.column import Column


class NumericColumn(Column[float]):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: list[float] = []

    def add_item(self, item: float):
        if not isinstance(item, (int, float)):
            raise TypeError(f"Item must be a number, got {type(item).__name__}")
        self.items.append(float(item))

    def write_to_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        column_nr: int,
    ):

        max_number = 0
        min_number = float("inf")
        for row, item in enumerate(self.items, start=1):
            worksheet.write(row, column_nr, item)
            max_number = max(max_number, item)
            min_number = min(min_number, item)

        if max_number > 1:
            worksheet.set_column(column_nr, column_nr, len(str(max_number)) + 0.5)
        else:
            worksheet.set_column(column_nr, column_nr, 3.5)
            worksheet.set_column(
                column_nr, column_nr, 5, workbook.add_format({"num_format": "0.00"})
            )

        worksheet.conditional_format(
            1,
            column_nr,
            len(self.items),
            column_nr,
            {
                "type": "3_color_scale",
            },
        )
