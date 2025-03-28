from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chat_log.chat_message import ChatMessage
    from chat_log.chat_message_question import QuestionPurpose, QuestionType


class ChatMessageAnalyser(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_question_purpose(self, message: "ChatMessage") -> "QuestionPurpose":
        pass

    @abstractmethod
    def get_question_type(self, message: "ChatMessage") -> "QuestionType":
        pass
