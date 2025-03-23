from chat_log.chat_activity import ChatActivity
from chat_log.chat_message_answer import ChatMessageAnswer
from chat_log.chat_message_question import ChatMessageQuestion


class ChatInteraction(ChatActivity):
    """
    Question of user with response of AI
    """

    def __init__(self, messages):
        super().__init__(messages)

    def check_invariants(self):
        super().check_invariants()

        # Check if the first message is a question
        assert isinstance(self.messages[0], ChatMessageQuestion), "First message should be a question"

        # Check if the second message is an answer
        assert isinstance(self.messages[1], ChatMessageAnswer), "Second message should be an answer"

        # Check if there are only two messages
        assert len(self.messages) == 2, "There should be only two messages"
    
    def get_question(self) -> ChatMessageQuestion:
        message = self.messages[0]
        assert isinstance(message, ChatMessageQuestion)
        return message
    
    def get_answer(self) -> ChatMessageAnswer:
        message = self.messages[1]
        assert isinstance(message, ChatMessageAnswer)
        return message

    def get_waiting_time(self):
        return self.messages[1].time - self.messages[0].time

