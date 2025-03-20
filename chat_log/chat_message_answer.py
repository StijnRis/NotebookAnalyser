from datetime import datetime
from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_message import ChatMessage


class ChatMessageAnswer(ChatMessage):
    """
    A response to a chat message
    """

    def __init__(
        self,
        time: datetime,
        body: str,
        chat_message_analyser: ChatMessageAnalyser,
    ):
        super().__init__(
            time, body, chat_message_analyser
        )

    def is_question(self):
        return False

    def is_answer(self):
        return True
