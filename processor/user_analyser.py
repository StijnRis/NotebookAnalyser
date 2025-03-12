from report.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class UserAnalyser:
    """
    Generate a report about a user
    """

    def __init__(self):
        self.data = []

    def analyse_user(self, user: User):
        username = user.username
        message_count = user.get_chat_log().get_amount_of_messages()

        user_data = {
            "Username": username,
            "Message Count": message_count,
        }

        self.data.append(user_data)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Users Report", self.data)
