from datetime import timedelta
from typing import Any

from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from report.column.column import Column
from report.column.plots_column import PlotsColumn
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
        columns.extend([PlotsColumn(goal.name) for goal in learning_goals])
        self.sheet.add_columns(columns)

    def analyse_user(self, user: User):
        username = user.get_username()
        workspace_log = user.get_workspace_log()

        user_data: dict[str, Any] = {"Username": username}

        for learning_goal in self.learning_goals:
            progression = workspace_log.get_learning_goal_progression(learning_goal)
            progression = (
                progression.convert_to_progression_with_timedelta().remove_idle_time(
                    timedelta(minutes=5)
                )
            ).convert_to_list_of_tuples()

            user_data[f"{learning_goal.name}"] = progression

        self.sheet.add_row(user_data)
