from analyser.analyser import Analyser
from chat_log.chat_interaction import ChatInteraction
from report.column.enum_column import EnumColumn
from report.column.text_column import TextColumn
from report.column.timedelta_column import TimedeltaColumn
from user.user import User


class InteractionAnalyser(Analyser):
    """
    Generate report of a user question
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns(
            [
                TextColumn("question"),
                TextColumn("answer"),
                TimedeltaColumn("waiting time"),
                EnumColumn("question type"),
                EnumColumn("purpose"),
            ]
        )

    def analyze_interaction(self, message: ChatInteraction):
        question = message.get_question().body
        answer = message.get_answer().body
        waiting_time = message.get_waiting_time()

        self.sheet.add_row(
            {
                "question": question,
                "answer": answer,
                "waiting time": waiting_time,
                "question type": message.get_question().get_question_type(),
                "purpose": message.get_question().get_question_purpose(),
            }
        )

    def analyse_user(self, user: User):
        messages = user.chat_log.get_interactions()
        for interaction in messages:
            self.analyze_interaction(interaction)
