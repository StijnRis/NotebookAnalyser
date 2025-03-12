import re
from datetime import datetime
from typing import List, Optional

from chat_log.chat_message import ChatMessage
from chat_log.chat_user import ChatUser


class ChatActivity:
    """
    Collection of chat messages.

    """

    def __init__(
        self,
        messages: list[ChatMessage],
        users: dict[str, ChatUser],
    ):
        self.messages: list[ChatMessage] = messages
        self.users: dict[str, ChatUser] = users

        self.messages.sort(key=lambda x: x.time)

        self.check_invariants()

    def check_invariants(self):
        # Check if messages are sorted by time
        for i in range(len(self.messages) - 1):
            assert self.messages[i].time <= self.messages[i + 1].time

    def get_questions(self):
        messages = [message for message in self.messages if message.is_question()]
        return ChatActivity(messages, self.users)

    def get_answers(self):
        messages = [message for message in self.messages if message.is_answer()]
        return ChatActivity(messages, self.users)

    def get_amount_of_messages(self):
        return len(self.messages)

    def get_messages_length(self):
        length = 0
        for message in self.messages:
            length += message.get_message_length()
        return length

    def get_activity_between(self, start: datetime, end: datetime):
        return ChatActivity(
            [message for message in self.messages if start <= message.time <= end],
            self.users,
        )

    def get_code_snippets(
        self, include_questions: bool = True, include_answers: bool = True
    ):
        codes: List[str] = []
        for message in self.messages:
            if (include_questions and message.is_question()) or (
                include_answers and message.is_answer()
            ):
                matches = re.finditer(
                    r"(\`\`\`python|\`)((.|\n)+?)\`{1,3}", message.body, re.DOTALL
                )
                for match in matches:
                    code_snippet = match.group(2)
                    codes.append(code_snippet.strip())

        return codes

    def get_generated_code_snippets(self):
        return self.get_code_snippets(False, True)

    def get_send_code_snippets(self):
        return self.get_code_snippets(True, False)

    def get_list_of_messages(self):
        messages = []
        for message in self.messages:
            if message.is_question():
                text = f"{self.users[message.sender].name} asked: {message.body}"
                messages.append(text)
            elif message.is_answer():
                text = f"{self.users[message.sender].name} answered: {message.body}"
                messages.append(text)

        return messages

    def get_interactions(self):
        from chat_log.chat_interaction import ChatInteraction  # avoid circular import

        interactions: List[ChatInteraction] = []
        for i in range(0, len(self.messages) - 1):
            if self.messages[i].is_question() and self.messages[i + 1].is_answer():
                interactions.append(
                    ChatInteraction(
                        [self.messages[i], self.messages[i + 1]], self.users
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

