from datetime import timedelta

from chat_log.chat_message import ChatMessage
from report.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class QuestionAnalyser:
    """
    Generate report of a user question
    """

    def __init__(self):
        self.data = []

    def analyze_message(self, user: User, message: ChatMessage):
        body = message.body
        purpose = message.get_question_purpose()
        question_type = message.get_question_type()
        time = message.time
        active_notebook = user.get_notebook_log().get_active_file_at(time)
        ast_progression, output_progression, code_progression = (
            active_notebook.get_progressions()
        )
        output_progression_working_time = (
            output_progression.convert_to_notebook_progression().remove_idle_time()
        )

        current_output_progression = output_progression.get_progression_at(time)
        output_progression_in_10_minutes = output_progression.get_progression_at(
            time + timedelta(minutes=10)
        )

        self.data.append(
            {
                "Question": body,
                "Question type": question_type,
                "Purpose": purpose,
                "Output progression in next 10 minutes": output_progression_in_10_minutes
                - current_output_progression,
            }
        )

    def analyse_messages_of_user(self, user: User):
        messages = user.chat_log.get_questions().messages
        for question in messages:
            self.analyze_message(user, question)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Questions Report", self.data)
