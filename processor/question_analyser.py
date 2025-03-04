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

    def analyze_message(self, message: ChatMessage):
        print(f"Processing message {message.id}")
        body = message.body
        purpose = message.get_question_purpose()
        question_type = message.get_question_type()
        self.data.append(
            {
                "question": body,
                "length": len(body),
                "question_type": question_type,
                "purpose": purpose,
            }
        )

    def analyze_messages_of_user(self, user: User):
        print(f"Processing user {user.username}")
        messages = user.chat_log.get_questions().messages
        for question in messages:
            self.analyze_message(question)

    def analyse_messages_of_users(self, users: Users):
        for user in users.get_users():
            self.analyze_messages_of_user(user)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Questions Report", self.data)
