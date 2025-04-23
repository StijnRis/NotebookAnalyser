from analyser.analyser import Analyser
from report.column.datetime_column import DatetimeColumn
from report.column.text_column import TextColumn
from user.user import User


class RunTimeAnalyser(Analyser):
    """
    Generate report about the runtime errors
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns(
            [
                TextColumn("Username"),
                TextColumn("File"),
                DatetimeColumn("Time"),
                TextColumn("Code version"),
                TextColumn("Error fix"),
                TextColumn("Error name"),
                TextColumn("Error value"),
                TextColumn("Error cleaned traceback"),
                TextColumn("Error type"),
            ]
        )

    def analyse_user(self, user: User):
        username = user.get_username()
        notebook_activity = user.get_workspace_log()

        file_logs = notebook_activity.get_file_logs()

        for file_log in file_logs:
            file_execution_log = file_log.get_file_execution_log()
            runtime_errors = file_execution_log.get_runtime_errors()
            file_path = file_log.get_path()
            code_versions_log = file_log.get_code_version_log()

            for runtime_error in runtime_errors:
                time = runtime_error.get_time()
                code_version = code_versions_log.get_code_file_at(time)

                code_fix = file_log.get_code_fix_for_error(runtime_error)

                self.sheet.add_row(
                    {
                        "Username": username,
                        "File": file_path,
                        "Time": time,
                        "Code version": code_version.get_code(),
                        "Error fix": code_fix,
                        "Error name": runtime_error.get_error_name(),
                        "Error value": runtime_error.get_error_value(),
                        "Error cleaned traceback": runtime_error.get_cleaned_traceback(),
                        "Error type": runtime_error.get_error_type().name,
                    }
                )
