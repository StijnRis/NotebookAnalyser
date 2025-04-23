from analyser.analyser import Analyser
from processor.learning_goal.learning_goal import LearningGoal
from user.user import User


class LearningGoalAnalyser(Analyser):
    def __init__(self, learning_goals: list[LearningGoal]):
        super().__init__()
        self.learning_goals = learning_goals

    def analyse_user(self, user: User):
        """
        Analyze the learning goals and store the results in self.data.
        """
        

