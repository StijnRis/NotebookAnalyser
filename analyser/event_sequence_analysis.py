from analyser.analyser import Analyser


class EventSequenceAnalysis(Analyser):
    def __init__(self):
        super().__init__()

    def analyse_user(self, user):
        sequence = user.get_event_sequence()
        for i in range(len(sequence) - 1):
            from_event, to_event = sequence[i][1], sequence[i + 1][1]
            for item in self.data:
                if item["from_event"] == from_event:
                    if to_event not in item:
                        item[to_event] = 0
                    item[to_event] += 1
                    break
            else:
                new_item = {"from_event": from_event, to_event: 1}
                self.data.append(new_item)
    
    def preprocess_data(self):
        all_keys = set()
        for item in self.data:
            all_keys.update(item.keys())

        # Add missing data values
        for item in self.data:
            for key in all_keys:
                if key not in item:
                    item[key] = 0

        # Order keys
        for item in self.data:
            ordered_keys = ["from_event"] + sorted(k for k in all_keys if k != "from_event")
            ordered_item = {key: item[key] for key in ordered_keys}
            item.clear()
            item.update(ordered_item)
