
from datetime import datetime
from enum import Enum
from functools import lru_cache
from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_message import ChatMessage


class QuestionPurpose(Enum):
    EXECUTIVE = "executive"
    INSTRUMENTAL = "instrumental"
    NOT_DETECTED = "unable to detect the questions purpose"


class QuestionType(Enum):
    """Enumeration of different types of questions a chatbot might encounter."""

    ANSWER_TO_QUESTION_OF_CHATBOT = "The user is responding to a question asked by the chatbot rather than asking a new one."

    CODE_COMPREHENSION = "The user is asking for an explanation of a piece of code, how it works, or what it does."

    CONCEPT_COMPREHENSION = "The user is asking for an explanation of a theoretical or abstract concept, often related to programming, science, or another domain."

    ERROR_COMPREHENSION = "The user is asking for help in understanding an error message, its cause, and how to fix it."

    QUESTION_COMPREHENSION = "The user is asking for clarification about a question itself, such as what it means or how to interpret it."

    COPIED_QUESTION = "The user has copied and pasted a question from another source without modification."

    FIX_CODE = "The user is asking for help in correcting a bug, syntax issue, or logical error in a piece of code."

    TASK_DELEGATION = "The user is asking the chatbot to perform a specific task, such as generating code, writing a document, or performing an analysis."

    PASTED_CODE_WITHOUT_CONTEXT = "The user has pasted a piece of code without providing an explicit question or any context."

    OTHER = "The user's question does not fit into any of the predefined categories."

    NOT_DETECTED = "The chatbot is unable to determine the type of question due to ambiguity or lack of information."

class ChatMessageQuestion(ChatMessage):
    """
    A question in the chat log
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

    @lru_cache(maxsize=None)
    def get_question_purpose(self):
        return self.chat_message_analyser.get_question_purpose(self)

    @lru_cache(maxsize=None)
    def get_question_type(self):
        return self.chat_message_analyser.get_question_type(self)