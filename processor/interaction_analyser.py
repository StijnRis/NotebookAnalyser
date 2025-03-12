from chat_log.chat_interaction import ChatInteraction
from report.report_generator import ReportGenerator
from user.user import User
from user.users import Users


class InteractionAnalyser:
    """
    Generate report of a user question
    """

    def __init__(self):
        self.data = []

    def analyze_interaction(self, message: ChatInteraction):
        question = message.get_question().body
        answer = message.get_answer().body
        waiting_time = message.get_waiting_time()

        self.data.append(
            {
                "question": question,
                "answer": answer,
                "waiting time": waiting_time,
                "question type": message.get_question().get_question_type(),
                "purpose": message.get_question().get_question_purpose(),
            }
        )

    def analyse_interactions_of_user(self, user: User):
        messages = user.chat_log.get_interactions()
        for interaction in messages:
            self.analyze_interaction(interaction)

    def save_result_to_report(self, report: ReportGenerator):
        report.display_data("Interaction Report", self.data)
