from typing import Any

from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from report.column.column import Column
from report.column.column_plots_column import ColumnPlotsColumn
from report.column.line_plots_column import LinePlotsColumn
from report.column.text_column import TextColumn
from user.user import User


class LearningGoalsAnalyser(Analyser):
    """
    Generate report of user learning goals
    """

    def __init__(self, learning_goals: list[LearningGoal]):
        super().__init__()
        self.learning_goals = learning_goals
        columns: list[Column] = [TextColumn("Username")]
        for goal in learning_goals:
            columns.append(ColumnPlotsColumn(goal.name))
            columns.append(LinePlotsColumn(f"{goal.name} EWM"))
            
        self.sheet.add_columns(columns)

    def analyse_user(self, user: User):
        username = user.get_username()
        workspace_log = user.get_workspace_log()

        user_data: dict[str, Any] = {"Username": username}

        active_periods = workspace_log.get_active_periods()
        progressions = workspace_log.get_learning_goals_progression(self.learning_goals)
        for i, learning_goal in enumerate(self.learning_goals):
            progression = (
                progressions[i].select_periods(active_periods, 0, 0)
            ).convert_to_list_of_tuples()

            user_data[f"{learning_goal.name}"] = progression

            ewm = (
                progressions[i]
                .convert_to_exponential_weighted_moving_average(0.5)
                .select_periods(active_periods, 0, 1)
                .convert_to_list_of_tuples()
            )

            user_data[f"{learning_goal.name} EWM"] = ewm

        self.sheet.add_row(user_data)
