from typing import List

from processor.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class UsersNotebooksAnalyser:
    """
    Analyse multiple users and generate a report.
    """

    def __init__(self):
        self.data = []

    def analyse_user(self, user: User):
        print(f"Analyzing user {user.username}")
        notebook_activity = user.get_notebook_log()

        notebook_files = notebook_activity.split_by_file()

        for notebook_file in notebook_files:
            times, ast_progression, output_progression, code_progression = (
                notebook_file.get_progressions()
            )

            # times, ast_progression, output_progression, code_progression = [1, 2, 3, 4], [10, 20, 30, 40], [100, 200, 300, 400], [1000, 2000, 3000, 4000]

            user_data = {
                "Username": user.username,
                "File": notebook_file.get_file_path(),
                "Tab switches": notebook_file.get_amount_of_tab_switches(),
                "Edit cycles": notebook_file.get_amount_of_edit_cycles(),
                "Executions": notebook_file.get_amount_of_executions(),
                "Runtime errors": notebook_file.get_amount_of_runtime_errors(),
                "Start time": notebook_file.get_start_time(),
                "End time": notebook_file.get_end_time(),
                "Completion time": notebook_file.get_completion_time(),
                "AST progression": (times, ast_progression),
                "Output progression": (times, output_progression),
                "Code progression": (times, code_progression),
            }

            self.data.append(user_data)

    def analyse_users(self, users: Users):
        for user in users.get_users():
            self.analyse_user(user)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("User Notebooks", self.data)