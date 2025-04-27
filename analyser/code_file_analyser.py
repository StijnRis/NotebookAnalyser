from datetime import timedelta

from analyser.analyser import Analyser
from report.column.datetime_column import DatetimeColumn
from report.column.numeric_column import NumericColumn
from report.column.plots_column import PlotsColumn
from report.column.text_column import TextColumn
from report.column.time_period_column import TimePeriodColumn
from report.column.timedelta_column import TimedeltaColumn
from user.user import User


class CodeFileAnalyser(Analyser):
    """
    Generate report of code files
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns(
            [
                TextColumn("Username"),
                TextColumn("File"),
                DatetimeColumn("Start passive time"),
                DatetimeColumn("Start active time"),
                DatetimeColumn("End active time"),
                DatetimeColumn("End passive time"),
                TimePeriodColumn("Active periods"),
                NumericColumn("Amount of editing events"),
                NumericColumn("Tab switches"),
                TimedeltaColumn("Completion time"),
                TimedeltaColumn("Open time"),
                TimedeltaColumn("Usage time"),
                NumericColumn("Amount of saves"),
                PlotsColumn("Code progression"),
                NumericColumn("Executions"),
                NumericColumn("Runtime errors"),
                PlotsColumn("Output progression"),
            ]
        )

    def analyse_user(self, user: User):
        username = user.get_username()
        workspace_log = user.get_workspace_log()

        file_logs = workspace_log.get_file_logs()

        for file_log in file_logs:
            output_progression = (
                file_log.get_file_execution_log().get_output_progression()
            )
            code_progression = file_log.get_code_version_log().get_code_progression()
            # ast_progression = file_log.get_ast_progression()

            active_periods = file_log.get_active_periods()

            output_progression_working_time = (
                output_progression.convert_to_progression_with_timedelta().remove_idle_time(
                    timedelta(minutes=5)
                )
            ).convert_to_list_of_tuples()
            code_progression_working_time = (
                code_progression.convert_to_progression_with_timedelta().remove_idle_time(
                    timedelta(minutes=5)
                )
            ).convert_to_list_of_tuples()
            # ast_progression_working_time = (
            #     ast_progression.convert_to_progression_with_timedelta().remove_idle_time(
            #         timedelta(minutes=5)
            #     )
            # ).convert_to_list_of_tuples()

            # ast_gradient = ast_progression_working_time.get_gradient()
            # output_gradient = output_progression_working_time.get_gradient()
            # code_gradient = code_progression_working_time.get_gradient()

            self.sheet.add_row(
                {
                    "Username": username,
                    "File": file_log.get_path(),
                    "Start passive time": file_log.get_start_passive_time(),
                    "Start active time": file_log.get_start_active_time(),
                    "End active time": file_log.get_end_active_time(),
                    "End passive time": file_log.get_end_passive_time(),
                    "Active periods": active_periods,
                    "Amount of editing events": file_log.get_editing_log().get_amount_of_events(),
                    "Tab switches": file_log.get_editing_log().get_amount_of_tab_switches(),
                    "Completion time": file_log.get_editing_log().get_total_time(),
                    "Open time": file_log.get_editing_log().get_total_time(),
                    "Usage time": file_log.get_editing_log().get_total_editing_time(),
                    "Amount of saves": file_log.get_code_version_log().get_amount_of_code_files(),
                    "Code progression": code_progression_working_time,
                    # "AST progression": ast_progression_working_time,
                    "Executions": file_log.get_file_execution_log().get_amount_of_executions(),
                    "Runtime errors": file_log.get_file_execution_log().get_amount_of_runtime_errors(),
                    "Output progression": output_progression_working_time,
                    # "AST gradient": ast_gradient,
                    # "Output gradient": output_gradient,
                    # "Code gradient": code_gradient,
                }
            )
