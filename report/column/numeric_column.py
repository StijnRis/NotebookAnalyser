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
        worksheet.set_column(column_nr, column_nr, 5)
        
        for row, item in enumerate(self.items, start=1):
            worksheet.write(row, column_nr, item)

        worksheet.conditional_format(
            1,
            column_nr,
            len(self.items),
            column_nr,
            {
                "type": "3_color_scale",
                "min_type": "num",
                "mid_type": "num",
                "max_type": "num",
            },
        )
