from analyser.analyser import Analyser
from report.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class UserAnalyser(Analyser):
    """
    Generate a report about a user
    """

    def __init__(self):
        super().__init__()

    def analyse_user(self, user: User):
        user_data = {
            "Username": user.username,
            "Message Count": user.get_chat_log().get_amount_of_messages(),
            "Editing Time": user.get_notebook_log().get_editing_time(),
            "Tab switches": user.get_notebook_log().get_amount_of_tab_switches(),
            "Executions": user.get_notebook_log().get_amount_of_executions(),
            "Runtime errors": user.get_notebook_log().get_amount_of_runtime_errors(),
        }

        self.data.append(user_data)