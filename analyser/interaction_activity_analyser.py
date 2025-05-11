from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from report.column.boolean_column import BooleanColumn
from report.column.datetime_column import DatetimeColumn
from report.column.enum_column import EnumColumn
from report.column.multiline_text_column import MultilineTextColumn
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn
from report.column.timedelta_column import TimedeltaColumn
from user.user import User


class InteractionActivityAnalyser(Analyser):
    """
    Generate report of a user question
    """

    def __init__(self, learning_goals: list[LearningGoal]):
        super().__init__()
        self.learning_goals = learning_goals
        self.sheet.add_columns(
            [
                TextColumn("Username"),
                DatetimeColumn("Time"),
                MultilineTextColumn("Question"),
                MultilineTextColumn("Answer"),
                EnumColumn("Question type"),
                EnumColumn("Purpose"),
                TextColumn("Learning goals"),
                TimedeltaColumn("Waiting time"),
                NumericColumn("Question length"),
                NumericColumn("Answer length"),
                BooleanColumn("Code in question"),
                BooleanColumn("Code in answer"),
                TextColumn("Question language"),
                TextColumn("Answer language"),
                NumericColumn("Similarity to code"),
                NumericColumn("Output progression in next 10 minutes"),
            ]
        )

    def analyse_user(self, user: User):
        interactions = user.get_interaction_activities()

        for interaction_activity in interactions:
            interaction = interaction_activity.get_interaction()

            self.sheet.add_row(
                {
                    "Username": user.get_username(),
                    "Time": interaction.get_question().get_time(),
                    "Question": interaction.get_question().body,
                    "Answer": interaction.get_answer().body,
                    "Question type": interaction.get_question().get_question_type(),
                    "Purpose": interaction.get_question().get_question_purpose(),
                    "Learning goals": ", ".join(goal.name for goal in interaction.get_question().get_question_learning_goals(tuple(self.learning_goals))),
                    "Waiting time": interaction.get_waiting_time(),
                    "Question length": interaction.get_question().get_length(),
                    "Answer length": interaction.get_answer().get_length(),
                    "Question language": interaction.get_question().get_language(),
                    "Answer language": interaction.get_answer().get_language(),
                    "Code in question": interaction.get_question().contains_code(),
                    "Code in answer": interaction.get_answer().contains_code(),
                    "Similarity to code": interaction_activity.get_similarity_to_code(),
                    "Output progression in next 10 minutes": interaction_activity.get_progression_in_next_10_minutes(),
                }
            )
