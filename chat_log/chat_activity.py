import re
from datetime import datetime
from typing import Generic, List, TypeVar

from chat_log.chat_message import ChatMessage
from chat_log.chat_message_answer import ChatMessageAnswer
from chat_log.chat_message_question import ChatMessageQuestion

T = TypeVar("T", bound=ChatMessage)


class ChatActivity(Generic[T]):
    """
    Collection of chat messages.

    """

    def __init__(
        self,
        messages: list[T],
    ):
        self.messages = messages

        self.messages.sort(key=lambda x: x.time)

        self.check_invariants()

    def get_messages(self):
        return self.messages

    def check_invariants(self):
        # Check if messages are sorted by time
        for i in range(len(self.messages) - 1):
            assert self.messages[i].time <= self.messages[i + 1].time

    def get_questions(self) -> "ChatActivity[ChatMessageQuestion]":
        messages = [
            message
            for message in self.messages
            if isinstance(message, ChatMessageQuestion)
        ]
        return ChatActivity(messages)

    def get_answers(self) -> "ChatActivity[ChatMessageAnswer]":
        messages = [
            message
            for message in self.messages
            if isinstance(message, ChatMessageAnswer)
        ]
        return ChatActivity(messages)

    def get_amount_of_messages(self) -> int:
        return len(self.messages)

    def get_total_messages_length(self) -> int:
        length = 0
        for message in self.messages:
            length += message.get_length()
        return length

    def get_activity_between(self, start: datetime, end: datetime):
        return ChatActivity(
            [message for message in self.messages if start <= message.time <= end],
        )

    def get_included_code_snippets(self):
        codes: List[str] = []
        for message in self.messages:
            matches = re.finditer(
                r"(\`\`\`python|\`)((.|\n)+?)\`{1,3}", message.body, re.DOTALL
            )
            for match in matches:
                code_snippet = match.group(2)
                codes.append(code_snippet.strip())

        return codes

    def get_interactions(self):
        from chat_log.chat_interaction import ChatInteraction  # avoid circular import

        interactions: List[ChatInteraction] = []
        for i in range(0, len(self.messages) - 1):
            if isinstance(self.messages[i], ChatMessageQuestion) and isinstance(
                self.messages[i + 1], ChatMessageAnswer
            ):
                interactions.append(
                    ChatInteraction([self.messages[i], self.messages[i + 1]])
                )

        return interactions

    def get_event_sequence(self):
        """Get sequence of events in the chat log.
        Each event is a tuple with the time and the type of event.
        """
        sequence: list[tuple[datetime, str]] = []
        for message in self.messages:
            if isinstance(message, ChatMessageQuestion):
                sequence.append((message.time, "Question"))
            elif isinstance(message, ChatMessageAnswer):
                sequence.append((message.time, "Answer"))
            else:
                raise ValueError(f"Unknown message type: {type(message)}")
        return sequence
