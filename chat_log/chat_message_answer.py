from datetime import datetime
from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_message import ChatMessage
from chat_log.chat_user import ChatUser


class ChatMessageAnswer(ChatMessage):
    """
    A response to a chat message
    """

    def __init__(
        self,
        chat_message_analyser: ChatMessageAnalyser,
        time: datetime,
        body: str,
        sender: ChatUser,
        deleted: bool,
        edited: bool,
    ):
        super().__init__(
            chat_message_analyser, time, body, sender, deleted, edited
        )
