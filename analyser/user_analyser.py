from analyser.analyser import Analyser
from user.user import User


class UserAnalyser(Analyser):
    """
    Generate a report about a user
    """

    def __init__(self):
        super().__init__()

    def analyse_user(self, user: User):
        user_data = {
            "Username": user.username,
            "Message count": user.get_chat_log().get_amount_of_messages(),
            "File count": user.get_workspace_log().get_amount_of_files(),
            # "Notebook open Time": user.get_workspace_log().get_notebook_open_time(),
            # "Notebook usage Time": user.get_workspace_log().get_notebook_usage_time(),
            # "Tab switches": user.get_workspace_log().get_amount_of_tab_switches(),
            # "Executions": user.get_workspace_log().get_amount_of_executions(),
            # "Runtime errors": user.get_workspace_log().get_amount_of_runtime_errors(),
        }

        self.data.append(user_data)
