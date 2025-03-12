from difflib import SequenceMatcher

from chat_log.chat_activity import ChatActivity
from notebook_log.notebook_cell_activity import NotebookCellActivity


class CellActivity:
    """
    All chat and notebook logs related to a single cell.
    """

    def __init__(
        self,
        notebook_activity: NotebookCellActivity,
        chat_activity: ChatActivity,
    ):
        self.notebook_activity = notebook_activity
        self.chat_activity = chat_activity

    def get_used_ai_code(self):
        generated_codes = self.chat_activity.get_generated_code_snippets()
        code = self.notebook_activity.get_content_at(
            self.notebook_activity.get_end_time()
        ).get_source()

        # Find all code snippets that are in the notebook state
        snippets = []
        for generated_code in generated_codes:
            if generated_code in code:
                snippets.append(generated_code)

        return snippets

    def get_similirities_between_ai_code_and_cell(self, time):
        code = self.notebook_activity.get_content_at(time).get_source()
        generated_codes = self.chat_activity.get_generated_code_snippets()

        # Find all code snippets that are in the notebook state
        similarities = []
        for generated_code in generated_codes:
            similarities.append(SequenceMatcher(None, generated_code, code).ratio())

        return similarities

    def get_overview(self, level=1):
        similarities = [
            round(x, 2)
            for x in self.get_similirities_between_ai_code_and_cell(
                self.notebook_activity.get_end_time()
            )
        ]
        return (
            f"{'#' * level} Summary for cell {self.notebook_activity.get_cell_id()} with index {self.notebook_activity.get_cell_index()}\n\n"
            f"Similarities between generated code snippets and final cell state: {similarities}\\\n"
            f"Used AI code: {self.get_used_ai_code()}\\\n"
            f"{self.notebook_activity.get_overview(level + 1)}\n"
            f"{self.chat_activity.get_overview(level + 1)}"
        )
