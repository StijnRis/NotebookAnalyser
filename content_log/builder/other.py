    def get_cell_activities(self):
        return self.code_snippets
        cell_index_to_activity: dict[int, List[NotebookLogEntry]] = {}

        for entry in self.events:
            event_name = entry.eventDetail.eventName

            eventInfo = entry.eventDetail.eventInfo
            if eventInfo is None:
                print(f"No event info found for {event_name}")
                continue

            if eventInfo.cells is not None:
                cells = eventInfo.cells
                cell_ids = [cell.index for cell in cells]
            else:
                if eventInfo.index is None:
                    print(f"No cell index found for {event_name}")
                    continue
                cell_ids = [eventInfo.index]

            for cell_id in cell_ids:
                if cell_id not in cell_index_to_activity:
                    cell_index_to_activity[cell_id] = []

                cell_index_to_activity[cell_id].append(entry)

        notebook_cell_activities: list[CodeSnippetActivity] = []
        for cell_id, entries in cell_index_to_activity.items():
            notebook_cell_activities.append(CodeSnippetActivity(entries))

        return notebook_cell_activities