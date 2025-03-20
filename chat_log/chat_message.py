from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_user import ChatUser



class ChatMessage(ABC):
    """
    A single chat message
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
        self.chat_message_analyser = chat_message_analyser
        self.type = type
        self.time = time
        self.body = body
        self.sender = sender
        self.deleted = deleted
        self.edited = edited

    def get_length(self):
        return len(self.body)

    @abstractmethod
    def is_question(self):
        pass

    @abstractmethod
    def is_answer(self):
        pass

    def __str__(self):
        return f"{self.sender} ({self.time}): {self.body}"



