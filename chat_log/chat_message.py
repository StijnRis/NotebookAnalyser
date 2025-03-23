from abc import ABC, abstractmethod
from datetime import datetime

from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser


class ChatMessage(ABC):
    """
    A single chat message
    """

    def __init__(
        self,
        time: datetime,
        body: str,
        chat_message_analyser: ChatMessageAnalyser,
    ):
        self.time = time
        self.body = body
        self.chat_message_analyser = chat_message_analyser
    
    def get_time(self):
        return self.time
    
    def get_body(self):
        return self.body

    def get_length(self):
        return len(self.body)