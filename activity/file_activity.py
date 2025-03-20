from difflib import SequenceMatcher

from chat_log.chat_activity import ChatActivity
from notebook_log.notebook_file_activity import NotebookFileActivity


class FileActivity:
    """
    All chat and file logs related to a single file.
    """

    def __init__(
        self,
        notebook_file_activity: NotebookFileActivity,
        chat_activity: ChatActivity,
    ):
        self.notebook_file_activity = notebook_file_activity
        self.chat_activity = chat_activity

    def get_notebook_file_activity(self):
        return self.notebook_file_activity
    
    def get_chat_activity(self):
        return self.chat_activity

    def get_used_ai_code(self):
        generated_codes = self.chat_activity.get_generated_code_snippets()
        code = self.notebook_file_activity.get_content_at(
            self.notebook_file_activity.get_end_time()
        ).get_source_as_string()

        # Find all code snippets that are in the notebook state
        snippets = []
        for generated_code in generated_codes:
            if generated_code in code:
                snippets.append(generated_code)

        return snippets

    def get_similarities_between_ai_code_and_cell(self, time):
        code = self.notebook_file_activity.get_content_at(time).get_source_as_string()
        generated_codes = self.chat_activity.get_generated_code_snippets()

        # Find all code snippets that are in the notebook state
        similarities = []
        for generated_code in generated_codes:
            similarities.append(SequenceMatcher(None, generated_code, code).ratio())

        return similarities