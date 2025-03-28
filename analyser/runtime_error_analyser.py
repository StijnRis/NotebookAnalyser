from analyser.analyser import Analyser
from content_log.execution_log.execution_result import ExecutionErrorResult
from user.user import User


class RunTimeAnalyser(Analyser):
    """
    Generat report about the runtime errors
    """

    def __init__(self):
        super().__init__()

    def analyse_user(self, user: User):
        username = user.get_username()
        notebook_activity = user.get_workspace_log()

        file_logs = notebook_activity.get_file_logs()

        for file_log in file_logs:
            file_execution_log = file_log.get_file_execution_log()
            runtime_errors = file_execution_log.get_runtime_errors()

            for runtime_error in runtime_errors:
                self.analyse_runtime_error(runtime_error, username, file_log.get_path())

    def analyse_runtime_error(
        self, runtime_error: ExecutionErrorResult, username: str, file_path: str
    ):
        runtime_error_data = {
            "Username": username,
            "File": file_path,
            "Error time": runtime_error.get_time(),
            "Error name": runtime_error.get_error_name(),
            "Error value": runtime_error.get_error_value(),
            "Error traceback": runtime_error.get_traceback(),
            "Error cleaned traceback": runtime_error.get_cleaned_traceback(),
            "Error type": runtime_error.get_error_type().name,
        }

        self.data.append(runtime_error_data)
