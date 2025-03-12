from chat_log.chat_activity import ChatActivity


class ChatInteraction(ChatActivity):
    """
    Question of user with response of AI
    """

    def __init__(self, messages, users):
        super().__init__(messages, users)

    def check_invariants(self):
        super().check_invariants()

        # Check if the first message is a question
        assert self.messages[0].is_question(), "First message should be a question"

        # Check if the second message is an answer
        assert self.messages[1].is_answer(), "Second message should be an answer"

        # Check if there are only two messages
        assert len(self.messages) == 2, "There should be only two messages"
    
    def get_question(self):
        return self.messages[0]
    
    def get_answer(self):
        return self.messages[1]

    def get_waiting_time(self):
        return self.messages[1].time - self.messages[0].time

