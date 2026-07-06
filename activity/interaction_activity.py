import difflib
from datetime import datetime, timedelta

from chat_log.chat_interaction import ChatInteraction
from content_log.file_log import FileLog
from content_log.workspace_log import WorkspaceLog
from processor.learning_goal import learning_goal
from processor.learning_goal.learning_goal import LearningGoal


class InteractionActivity:
    def __init__(
        self,
        interaction: ChatInteraction,
        previous_code_log: FileLog | None,
        next_code_log: FileLog | None,
        workspace_log: WorkspaceLog,
        learning_goals: list[LearningGoal],
    ):
        self.interaction = interaction
        self.previous_code_log = previous_code_log
        self.next_code_log = next_code_log
        self.workspace_log = workspace_log
        self.learning_goals = learning_goals

    def get_interaction(self) -> ChatInteraction:
        return self.interaction

    def get_previous_code_log(self) -> FileLog | None:
        return self.previous_code_log

    def get_next_code_log(self) -> FileLog | None:
        return self.next_code_log

    def get_workspace_log(self) -> WorkspaceLog:
        return self.workspace_log

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

    def get_increase_in_success_rate(self) -> float:
        if self.previous_code_log is None or self.next_code_log is None:
            return 0.0
        
        applied_learning_goals = self.interaction.get_question().get_question_learning_goals(tuple(self.learning_goals))

        progressions = self.workspace_log.get_learning_goals_progression(tuple(self.learning_goals))
        increases = []
        for i, progression in enumerate(progressions):
            if self.learning_goals[i] not in applied_learning_goals:
                continue
            if progression.get_total_count() == 0:
                continue
            progression_before = progression.select_period(datetime.min, self.interaction.get_question().get_time())
            progression_after = progression.select_period(self.interaction.get_question().get_time(), datetime.max)
            if progression_before.get_total_count() == 0 or progression_after.get_total_count() == 0:
                continue
            success_rate_before = progression_before.count_occurrences(1) / progression_before.get_total_count()
            success_rate_after = progression_after.count_occurrences(1) / progression_after.get_total_count()
            increases.append(success_rate_after - success_rate_before)
        
        return sum(increases) / len(increases) if increases else 0.0

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
