import difflib
from datetime import timedelta

from chat_log.chat_interaction import ChatInteraction
from content_log.file_log import FileLog
from processor.learning_goal.learning_goal import LearningGoal


class InteractionActivity:
    def __init__(
        self,
        interaction: ChatInteraction,
        previous_code_log: FileLog | None,
        next_code_log: FileLog | None,
    ):
        self.interaction = interaction
        self.previous_code_log = previous_code_log
        self.next_code_log = next_code_log

    def get_interaction(self) -> ChatInteraction:
        return self.interaction

    def get_previous_code_log(self) -> FileLog | None:
        return self.previous_code_log

    def get_next_code_log(self) -> FileLog | None:
        return self.next_code_log

    def get_progression_in_next_10_minutes(self) -> float:
        if self.next_code_log is None:
            return 0.0

        output_progression = (
            self.next_code_log.get_file_execution_log().get_output_progression()
        )
        output_progression_in_10_minutes = output_progression.get_progression_at(
            self.interaction.get_question().get_time() + timedelta(minutes=10)
        )
        current_output_progression = output_progression.get_progression_at(
            self.interaction.get_question().get_time()
        )
        return output_progression_in_10_minutes - current_output_progression

    def get_similarity_to_code(self) -> float:
        """
        Get all code snippets that are copied from the file
        """
        percentage_1 = 0
        percentage_2 = 0
        question = self.interaction.get_question().get_body()

        if self.previous_code_log is not None:
            code_1 = (
                self.previous_code_log.get_code_version_log()
                .get_code_file_at(self.interaction.get_question().get_time())
                .get_code()
            )
            percentage_1 = difflib.SequenceMatcher(None, code_1, question).ratio()

        if self.next_code_log is not None:
            code_2 = (
                self.next_code_log.get_code_version_log()
                .get_code_file_at(self.interaction.get_question().get_time())
                .get_code()
            )
            percentage_2 = difflib.SequenceMatcher(None, code_2, question).ratio()

        return max(percentage_1, percentage_2)
