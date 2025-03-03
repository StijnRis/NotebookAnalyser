from datetime import datetime, timedelta

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name


class ReportGenerator:
    def __init__(self, file_path: str):
        self.workbook = xlsxwriter.Workbook(file_path)

    def display_data(self, worksheet_name: str, data: list[dict]):
        # Check that all have same keys
        keys = list(data[0].keys())
        for item in data:
            assert keys == list(item.keys()), "All items must have the same keys"

        # Split into keys with atomic values and keys with list values
        string_based_keys = []
        numeric_based_keys = []
        list_based_keys = []
        for key in keys:
            if isinstance(data[0][key], (int, float)):
                numeric_based_keys.append(key)
            elif isinstance(data[0][key], (str, datetime, timedelta)):
                string_based_keys.append(key)
            elif isinstance(data[0][key], tuple):
                list_based_keys.append(key)
            else:
                raise ValueError(f"Unsupported type: {type(data[0][key])}")

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

        # Create the worksheets for keys with multiple values
        multi_valued_worksheets = {}
        for key in list_based_keys:
            multi_valued_worksheets[key] = {
                "x": self.workbook.add_worksheet(f"{worksheet_name} - {key} (x)"),
                "y": self.workbook.add_worksheet(f"{worksheet_name} - {key} (y)"),
            }

            multi_valued_worksheets[key]["x"].hide()
            multi_valued_worksheets[key]["y"].hide()
        
        # Apply format to multi-valued columns
        for key in list_based_keys:
            main_worksheet.set_column(keys.index(key), keys.index(key), 20)

        # Apply colour scales to numeric columns
        for key in numeric_based_keys:
            main_worksheet.conditional_format(
                1,
                keys.index(key),
                len(data),
                keys.index(key),
                {
                    "type": "3_color_scale",
                    "min_type": "num",
                    "mid_type": "num",
                    "max_type": "num",
                },
            )

        # Write data
        for i, item in enumerate(data):
            for j, key in enumerate(keys):
                if key in string_based_keys:
                    main_worksheet.write(i + 1, j, item[key])
                elif key in numeric_based_keys:
                    main_worksheet.write(i + 1, j, item[key])
                elif key in list_based_keys:
                    worksheet_x = multi_valued_worksheets[key]["x"]
                    worksheet_y = multi_valued_worksheets[key]["y"]
                    worksheet_x.write_row(i + 1, 0, item[key][0])
                    worksheet_y.write_row(i + 1, 0, item[key][1])
                    end_column = xl_col_to_name(len(item[key][0]))
                    main_worksheet.add_sparkline(
                        i + 1,
                        j,
                        {
                            "range": f"'{worksheet_y.name}'!$A${i + 2}:${end_column}${i + 2}",
                            "date_axis": f"'{worksheet_x.name}'!$A${i + 2}:${end_column}${i + 2}",
                            "type": "line",
                        },
                    )

        # Format the entire worksheet as a table
        column_settings = [{"header": key} for key in keys]
        main_worksheet.add_table(
            0,
            0,
            len(data),
            len(keys) - 1,
            {"columns": column_settings, "style": "Table Style Medium 9"},
        )

    def close(self):
        self.workbook.close()
