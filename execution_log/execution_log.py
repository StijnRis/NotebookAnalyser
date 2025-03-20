class ExecutionLog():
    def __init__(self):
        pass

    def get_amount_of_executions(self):
        total = 0
        for entry in self.events:
            event_name = entry.eventDetail.eventName
            if event_name == NotebookEventName.CELL_EXECUTE:
                total += 1

        return total

    def get_amount_of_runtime_errors(self):
        total = 0
        for entry in self.events:
            event_name = entry.eventDetail.eventName
            if event_name == NotebookEventName.CELL_EXECUTE:
                eventInfo = entry.eventDetail.eventInfo
                assert eventInfo is not None, "eventInfo should not be None"
                if eventInfo.success == False:
                    total += 1

        return total

    def get_execution_results(self) -> List[tuple[datetime, bool]]:
        """
        Returns a list of tuples with the event time and execution result (success or failure).
        """
        results = []
        for entry in self.events:
            if entry.eventDetail.eventName == NotebookEventName.CELL_EXECUTE:
                event_time = entry.eventDetail.eventTime
                event_info = entry.eventDetail.eventInfo
                assert event_info is not None, "eventInfo should not be None"
                success = event_info.success
                results.append((event_time, success))
        return results
    
    def get_outputs(self):
        """
        Get the outputs of the notebook.
        """
        outputs: list[str] = []
        for cell in self.code_snippets:
            if cell.cell_type != "code":
                continue

            # Add output of cell
            total_output = ""
            for output in cell.outputs:
                total_output += output.to_string()
            outputs.append(total_output)

        return outputs
    
    def get_output_difference_ratio(self, other: "CodeSnippets"):
        """
        Compare output of two notebooks
        """

        output1 = self.get_outputs()
        output2 = other.get_outputs()

        return SequenceMatcher(None, output1, output2).ratio()