from datetime import datetime
from difflib import SequenceMatcher

from chat_log.chat_activity import ChatActivity
from content_log.file_log import FileLog


class FileActivity:
    """
    All chat and file logs related to a single file.
    """

    def __init__(
        self,
        file_log: FileLog,
        chat_activity: ChatActivity,
    ):
        self.file_log = file_log
        self.chat_activity = chat_activity

    def get_file_log(self):
        return self.file_log

    def get_chat_activity(self):
        return self.chat_activity

    def get_used_ai_code(self):
        generated_codes = self.chat_activity.get_answers().get_included_code_snippets()
        code_files = self.file_log.get_code_version_log().get_code_files()

        if len(code_files) == 0:
            return []

        code = code_files[-1].get_code()

        # Find all code snippets that are in the notebook state
        snippets = []
        for generated_code in generated_codes:
            if generated_code in code:
                snippets.append(generated_code)

        return snippets

    def get_similarities_between_ai_code_and_cell(self, time: datetime):
        generated_codes = self.chat_activity.get_answers().get_included_code_snippets()
        code = self.file_log.get_code_version_log().get_code_file_at(time).get_code()

        # Find all code snippets that are in the notebook state
        similarities = []
        for generated_code in generated_codes:
            similarities.append(SequenceMatcher(None, generated_code, code).ratio())

        return similarities
