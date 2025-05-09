from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from report.column.boolean_column import BooleanColumn
from report.column.datetime_column import DatetimeColumn
from report.column.multiline_text_column import MultilineTextColumn
from report.column.numeric_column import NumericColumn
from report.column.text_column import TextColumn
from user.user import User


class EditRunCycleAnalyser(Analyser):
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
                MultilineTextColumn("Code"),
                MultilineTextColumn("Result"),
                MultilineTextColumn("Modifications"),
                MultilineTextColumn("Applied AST items"),
                MultilineTextColumn("Applied learning goals"),
                TextColumn("Learning goal in error"),
                TextColumn("Learning goal in error 2"),
            ]
        )

    def analyse_user(self, user: User):
        username = user.get_username()

        file_logs = user.get_workspace_log().get_file_logs()
        for file_log in file_logs:
            edit_run_cycles = file_log.get_all_edit_run_cycles()

            for edit_run_cycle in edit_run_cycles:
                self.sheet.add_row(
                    {
                        "Username": username,
                        "File": edit_run_cycle.get_code().get_path(),
                        "Timestamp": edit_run_cycle.get_execution()
                        .get_time()
                        .timestamp(),
                        "Time": edit_run_cycle.get_execution().get_time(),
                        "Success": edit_run_cycle.get_execution().get_error() is None,
                        "Code": edit_run_cycle.get_code().get_code(),
                        "Result": edit_run_cycle.get_execution().get_content(),
                        "Modifications": edit_run_cycle.get_modifications(),
                        "Applied AST items": ", ".join(
                            type(item).__name__
                            for item in edit_run_cycle.get_applied_ast_items()
                        ),
                        "Applied learning goals": ", ".join(
                            goal.name
                            for goal in edit_run_cycle.get_applied_learning_goals(
                                self.learning_goals
                            )
                        ),
                        "Learning goal in error": ", ".join(goal.name for goal in edit_run_cycle.get_learning_goals_in_error()),
                        "Learning goal in error 2": ", ".join(goal.name for goal in edit_run_cycle.get_error_type_method_2(
                            self.learning_goals
                        )),
                    }
                )
