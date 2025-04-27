from datetime import timedelta

from analyser.analyser import Analyser
from chat_log.chat_message_question import ChatMessageQuestion
from report.column.enum_column import EnumColumn
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn
from user.user import User


class QuestionAnalyser(Analyser):
    """
    Generate report of a user question
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns(
            [
                TextColumn("Question"),
                EnumColumn("Question type"),
                EnumColumn("Purpose"),
                NumericColumn("Output progression in next 10 minutes"),
            ]
        )

    def analyze_message_question(
        self, user: User, message_question: ChatMessageQuestion
    ):
        body = message_question.body
        purpose = message_question.get_question_purpose()
        question_type = message_question.get_question_type()
        time = message_question.time
        active_file = user.get_workspace_log().get_active_file_at(time)

        current_output_progression = 0
        output_progression_in_10_minutes = 0
        if active_file is not None:
            output_progression = (
                active_file.get_file_execution_log().get_output_progression()
            )

            current_output_progression = output_progression.get_progression_at(time)
            output_progression_in_10_minutes = output_progression.get_progression_at(
                time + timedelta(minutes=10)
            )

        self.sheet.add_row(
            {
                "Question": body,
                "Question type": question_type,
                "Purpose": purpose,
                "Output progression in next 10 minutes": output_progression_in_10_minutes
                - current_output_progression,
            }
        )

    def analyse_user(self, user: User):
        messages = user.chat_log.get_questions().messages
        for question in messages:
            self.analyze_message_question(user, question)
