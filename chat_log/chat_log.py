from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_activity import ChatActivity
from chat_log.chat_message import ChatMessage


class ChatLog(ChatActivity):
    """
    A processed chat log containing messages and users.
    """

    def __init__(
        self,
        messages: list[ChatMessage],
        chat_message_analyser: ChatMessageAnalyser,
    ):
        super().__init__(messages)
        self.chat_message_analyser = chat_message_analyser
