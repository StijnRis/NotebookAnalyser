from analyser.analyser import Analyser
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn
from user.user import User


class UserAnalyser(Analyser):
    """
    Generate a report about a user
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns([
            TextColumn("Username"),
            NumericColumn("Message count"),
            NumericColumn("File count"),
        ])

    def analyse_user(self, user: User):
        self.sheet.add_row({
            "Username": user.username,
            "Message count": user.get_chat_log().get_amount_of_messages(),
            "File count": user.get_workspace_log().get_amount_of_files(),
            # "Notebook open Time": user.get_workspace_log().get_notebook_open_time(),
            # "Notebook usage Time": user.get_workspace_log().get_notebook_usage_time(),
            # "Tab switches": user.get_workspace_log().get_amount_of_tab_switches(),
            # "Executions": user.get_workspace_log().get_amount_of_executions(),
            # "Runtime errors": user.get_workspace_log().get_amount_of_runtime_errors(),
        })