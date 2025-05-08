from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from report.column.boolean_column import BooleanColumn
from report.column.datetime_column import DatetimeColumn
from report.column.multiline_text_column import MultilineTextColumn
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn
from user.user import User


class ExecutionAnalyser(Analyser):
    """
    Generate report about the runtime errors
    """

    def __init__(self, learning_goals: list[LearningGoal]):
        super().__init__()
        self.learning_goals = learning_goals
        self.sheet.add_columns(
            [
                TextColumn("Username"),
                TextColumn("File"),
                NumericColumn("Timestamp"),
                DatetimeColumn("Time"),
                BooleanColumn("Success"),
                MultilineTextColumn("Modifications"),
                MultilineTextColumn("Code"),
                MultilineTextColumn("Result"),
                TextColumn("Error on lines"),
            ]
        )

    def analyse_user(self, user: User):
        username = user.get_username()

        file_logs = user.get_workspace_log().get_file_logs()
        for file_log in file_logs:
            executions = file_log.get_file_execution_log().get_executions()
            file_path = file_log.get_path()
            code_versions_log = file_log.get_code_version_log()

            previous_code_version = None
            for execution in executions:
                time = execution.get_time()
                timestamp = time.timestamp()
                end_code_version = code_versions_log.get_code_file_at(time)

                modifications = ""
                if previous_code_version is not None:
                    modifications = end_code_version.get_code_difference(
                        previous_code_version
                    )

                line_numbers = []
                error = execution.get_error()
                if error is not None:
                    line_numbers = error.get_line_numbers()

                self.sheet.add_row(
                    {
                        "Username": username,
                        "File": file_path,
                        "Timestamp": timestamp,
                        "Time": time,
                        "Success": error is None,
                        "Modifications": modifications,
                        "Code": end_code_version.get_code(),
                        "Result": execution.get_content(),
                        "Error on lines": f"{line_numbers}",
                    }
                )

                previous_code_version = end_code_version
