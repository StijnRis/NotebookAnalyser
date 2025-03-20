import re
from datetime import datetime
from typing import List

from chat_log.chat_message import ChatMessage


class ChatActivity:
    """
    Collection of chat messages.

    """

    def __init__(
        self,
        messages: list[ChatMessage],
    ):
        self.messages: list[ChatMessage] = messages

        self.messages.sort(key=lambda x: x.time)

        self.check_invariants()

    def check_invariants(self):
        # Check if messages are sorted by time
        for i in range(len(self.messages) - 1):
            assert self.messages[i].time <= self.messages[i + 1].time

    def get_questions(self):
        messages = [message for message in self.messages if message.is_question()]
        return ChatActivity(messages)

    def get_answers(self):
        messages = [message for message in self.messages if message.is_answer()]
        return ChatActivity(messages)

    def get_amount_of_messages(self):
        return len(self.messages)

    def get_messages_length(self):
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
            if self.messages[i].is_question() and self.messages[i + 1].is_answer():
                interactions.append(
                    ChatInteraction(
                        [self.messages[i], self.messages[i + 1]]
                    )
                )

        return interactions

    def get_event_sequence(self):
        """Get sequence of events in the chat log.
        Each event is a tuple with the time and the type of event.
        """
        sequence: list[tuple[datetime, str]] = []
        for message in self.messages:
            if message.is_question():
                sequence.append((message.time, "Question"))
            elif message.is_answer():
                sequence.append((message.time, "Answer"))
        return sequence
