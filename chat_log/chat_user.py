from typing import Optional

from chat_log.chat_message import ChatMessage


class ChatUser:
    """
    User in the chat log.
    """

    def __init__(
        self,
        messages: list[ChatMessage]
    ):
        self.messages = messages

