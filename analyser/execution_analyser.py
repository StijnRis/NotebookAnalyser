import ast
from difflib import unified_diff
from analyser.analyser import Analyser
from content_log.execution_log.execution_result import ExecutionErrorResult
from user.user import User


class ExecutionAnalyser(Analyser):
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
            executions = file_execution_log.get_executions()
            file_path = file_log.get_path()
            code_versions_log = file_log.get_code_version_log()

            previous_successful_execution = None
            errors_before_succes: list[ExecutionErrorResult] = []
            for execution in executions:
                if isinstance(execution, ExecutionErrorResult):
                    errors_before_succes.append(execution)
                    continue

                if previous_successful_execution is None:
                    previous_successful_execution = execution
                    continue

                time = execution.get_time()
                code_version = code_versions_log.get_code_file_at(time)

                previous_code_version = code_versions_log.get_code_file_at(
                    previous_successful_execution.get_time()
                )

                differences = code_version.get_code_difference(previous_code_version)

                lines_changed = code_version.get_changes_per_line(previous_code_version)
                lines_changed = [line[1] for line in lines_changed if line[1] is not None]

                new_ast_items = code_version.get_sub_ast(lines_changed)
                new_ast_items_string = ast.dump(new_ast_items, indent=4)




                execution_data = {
                    "Username": username,
                    "File": file_path,
                    "Time": time,
                    "Code version": code_version.get_code(),
                    "Errors during making": "\n".join(
                        [error.get_cleaned_traceback() for error in errors_before_succes]
                    ),
                    "Differences": differences,
                    "AST differences": new_ast_items_string,
                }

                self.data.append(execution_data)

                previous_successful_execution = execution
                errors_before_succes.clear()
