class FileLog:
    def __init__(self):
        pass

    def get_all_saved_notebook_contents(self):
        """
        Returns a list of tuples with the event time and notebook content.
        """
        notebook_contents: List[tuple[datetime, NotebookContent]] = []
        for entry in self.events:
            if entry.notebookState.notebookContent is not None:
                notebook_contents.append(
                    (entry.eventDetail.eventTime, entry.notebookState.notebookContent)
                )

        return notebook_contents
    
        # TODO: This is a copy of the method in NotebookContent. Should be refactored
    def get_content_at(self, time: datetime):
        """
        Get the notebook content at a certain time.
        """
        cell_content = None
        cell_id = self.get_cell_id()

        # Loop through all events
        for entry in self.events:

            # Check if this event happened
            if entry.eventDetail.eventTime > time:
                continue

            # Check if entire notebook is saved
            current_notebook_content = entry.notebookState.notebookContent
            if current_notebook_content is not None:
                cells = current_notebook_content.cells
                for cell in cells:
                    if cell.id == cell_id:
                        cell_content = cell
            else:
                pass  # TODO handle
                # print(f"Unknown how to parse {entry.eventDetail.eventName} event")

        assert cell_content is not None, "No cell content found"
        return cell_content

    def get_similarity_between_cell_states(self, time1: datetime, time2: datetime):
        end_result = self.get_content_at(time1).get_source()
        current_result = self.get_content_at(time2).get_source()
        return SequenceMatcher(None, end_result, current_result).ratio()
    
    # TODO merge with cell_activity get content at
    def get_content_at(self, time: datetime):
        """
        Get the notebook content at a certain time.
        """
        notebook_content = None

        # Loop through all events
        for entry in self.events:
            current_notebook_content = entry.notebookState.notebookContent

            # Check if this event happened
            if entry.eventDetail.eventTime > time:
                continue

            # Check if entire notebook is saved
            if current_notebook_content is not None:
                notebook_content = current_notebook_content
            else:
                pass  # TODO handle
                # print(f"Unknown how to parse {entry.eventDetail.eventName} event")

        assert notebook_content is not None, "Notebook content should be found"

        return notebook_content

    @lru_cache(maxsize=None)
    def get_progressions(self):
        """
        Calculate the progression of the notebook
        """
        saved_contents = self.get_all_saved_notebook_contents()

        times: list[datetime] = []
        ast_progression: list[float] = []
        output_progression: list[float] = []
        code_progression: list[float] = []

        # Check if user has saved any notebook content
        if len(saved_contents) == 0:
            return (
                NotebookProgressionWithDatetime(times, ast_progression),
                NotebookProgressionWithDatetime(times, output_progression),
                NotebookProgressionWithDatetime(times, code_progression),
            )

        last_notebook_content = saved_contents[-1][1]

        for event_time, content in saved_contents:
            ast_difference = content.get_ast_difference_ratio(last_notebook_content)

            output_difference = content.get_output_difference_ratio(
                last_notebook_content
            )

            code_difference = content.get_code_difference_ratio(last_notebook_content)

            times.append(event_time)
            ast_progression.append(ast_difference)
            output_progression.append(output_difference)
            code_progression.append(code_difference)

        return (
            NotebookProgressionWithDatetime(times, ast_progression),
            NotebookProgressionWithDatetime(times, output_progression),
            NotebookProgressionWithDatetime(times, code_progression),
        )