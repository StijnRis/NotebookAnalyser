from analyser.analyser import Analyser
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn


class EventSequenceAnalysis(Analyser):
    def __init__(self):
        super().__init__()
        self.data: dict[str, dict[str, int]] = {}

    def analyse_user(self, user):
        sequence = user.get_event_sequence()
        for i in range(len(sequence) - 1):
            from_event, to_event = sequence[i][1], sequence[i + 1][1]
            if from_event not in self.data:
                self.data[from_event] = {}
            item = self.data[from_event]
            if to_event not in item:
                item[to_event] = 0
            item[to_event] += 1

    def preprocess_data(self):
        all_keys = set()
        for item in self.data:
            all_keys.add(item)
            all_keys.update(self.data[item].keys())
        ordered_keys = sorted(k for k in all_keys if k != "from_event")

        # Add missing data values
        for item in self.data:
            if item not in self.data:
                self.data[item] = {}
            item = self.data[item]
            for key in all_keys:
                if key not in item:
                    item[key] = 0

        # Add columns to the sheet
        self.sheet.add_columns(
            [
                TextColumn("from_event"),
                *[NumericColumn(key) for key in ordered_keys],
            ]
        )

        # Add rows to the sheet
        for item in ordered_keys:
            self.sheet.add_row(
                {
                    "from_event": item,
                    **{
                        key: self.data[item][key]
                        for key in ordered_keys
                        if key != "from_event"
                    },
                }
            )
