from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from processor.learning_goal.learning_goal import LearningGoal

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

    @abstractmethod
    def get_question_learning_goals(
        self, message: "ChatMessage", learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        pass
