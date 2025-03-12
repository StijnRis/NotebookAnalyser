from report.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class NotebookAnalyser:
    """
    Generate report of user notebook
    """

    def __init__(self):
        self.data = []

    def analyse_notebooks_of_user(self, user: User):
        username = user.get_username()
        notebook_activity = user.get_notebook_log()

        notebook_files = notebook_activity.split_by_file()

        for notebook_file in notebook_files:
            ast_progression, output_progression, code_progression = (
                notebook_file.get_progressions()
            )
            ast_progression_working_time = (
                ast_progression.convert_to_notebook_progression().remove_idle_time()
            )
            output_progression_working_time = (
                output_progression.convert_to_notebook_progression().remove_idle_time()
            )
            code_progression_working_time = (
                code_progression.convert_to_notebook_progression().remove_idle_time()
            )

            ast_gradient = ast_progression_working_time.get_gradient()
            output_gradient = output_progression_working_time.get_gradient()
            code_gradient = code_progression_working_time.get_gradient()

            user_data = {
                "Username": username,
                "File": notebook_file.get_file_path(),
                "Tab switches": notebook_file.get_amount_of_tab_switches(),
                "Edit cycles": notebook_file.get_amount_of_edit_cycles(),
                "Executions": notebook_file.get_amount_of_executions(),
                "Runtime errors": notebook_file.get_amount_of_runtime_errors(),
                "Start time": notebook_file.get_start_time(),
                "End time": notebook_file.get_end_time(),
                "Completion time": notebook_file.get_completion_time(),
                "AST progression": ast_progression_working_time,
                "Output progression": output_progression_working_time,
                "Code progression": code_progression_working_time,
                "AST gradient": ast_gradient,
                "Output gradient": output_gradient,
                "Code gradient": code_gradient,
            }

            self.data.append(user_data)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Notebooks Report", self.data)
