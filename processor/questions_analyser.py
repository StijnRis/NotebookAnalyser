from chat_log.chat_message import ChatMessage
from processor.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class QuestionsAnalyser:
    def __init__(self, report_generator: ReportGenerator):
        self.report_generator = report_generator
        self.data = []

    def process_message(self, message: ChatMessage):
        print(f"Processing message {message.id}")
        body = message.body
        purpose = message.get_question_purpose()
        question_type = message.get_question_type()
        self.data.append(
            {
                "question": body,
                "question_type": question_type,
                "purpose": purpose,
            }
        )

    def analyze_user(self, user: User):
        print(f"Processing user {user.username}")
        messages = user.chat_log.get_questions().messages
        for question in messages:
            self.process_message(question)

    def analyse_users(self, users: Users):
        for user in users.get_users():
            self.analyze_user(user)

        self.report_generator.display_data("Questions Report", self.data)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Questions", self.data)
