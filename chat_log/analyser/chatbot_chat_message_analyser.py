from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_message import ChatMessage
from chat_log.chat_message_question import QuestionPurpose, QuestionType
from chatbot import Chatbot
from processor.learning_goal.learning_goal import LearningGoal


class ChatbotChatMessageAnalyser(ChatMessageAnalyser):

    def __init__(self, chatbot: Chatbot):
        self.chatbot = chatbot

    def get_question_purpose(self, message: ChatMessage):
        query = f"You are an instructor that classifies questions into executive or instrumental. You first reason about them and then give your final verdict on the last line. Structure the last line as following: 'The question is of type [executive/instrumental]'. Classify the following message {message.body}"

        for i in range(3):
            if i == 0:
                response = self.chatbot.ask_question(query)
            else:
                response = self.chatbot.ask_question_without_cache(query)
            response = response.lower().strip()
            last_sentence = response.split("\n")[-1]

            if "executive" in last_sentence and "instrumental" not in last_sentence:
                return QuestionPurpose.EXECUTIVE
            elif "instrumental" in last_sentence and "executive" not in last_sentence:
                return QuestionPurpose.INSTRUMENTAL

        return QuestionPurpose.NOT_DETECTED

    def get_question_type(self, message: ChatMessage):
        explanations = "\n".join([f"{e.name}: {e.value}" for e in QuestionType])

        query = f"You are an instructor that classifies questions. You first reason about them and then give your final verdict on the last line. Structure the last line as following: 'The question is of type [question type]'. Choose from the following question types: {explanations} \n\n Classify the following message {message.body}"

        for i in range(3):
            if i == 0:
                response = self.chatbot.ask_question(query)
            else:
                response = self.chatbot.ask_question_without_cache(query)
            response = response.lower().strip()
            last_sentence = response.split("\n")[-1]

            detected_types = []
            for question_type in QuestionType:
                if question_type.name.lower() in last_sentence:
                    detected_types.append(question_type)

            if len(detected_types) == 1:
                return detected_types[0]

        return QuestionType.NOT_DETECTED

    def get_question_learning_goals(
        self, message: ChatMessage, learning_goals: list[LearningGoal]
    ):
        explanations = "\n".join([f"{e.name}: {e.description}" for e in learning_goals])
        query = f"You are an expert instructor that classifies about which learning goals a question is related to. You first reason about them and then give your final verdict on the last line. Structure the last line as following: 'The question is about [list of learning goals]'. Choose from the following learning goals: {explanations} \n\n Classify the following message {message.body}"
        query = f"Which learning goal is this message related to? Choose from the following options: \n{learning_goals}\n\n Only answer the chosen option. \n The message: \n\n{message.body}"

        for i in range(3):
            if i == 0:
                response = self.chatbot.ask_question(query)
            else:
                response = self.chatbot.ask_question_without_cache(query)
            response = response.lower().strip()
            last_sentence = response.split("\n")[-1]

            detected_goals = []
            for learning_goal in learning_goals:
                if learning_goal.name.lower() in last_sentence:
                    detected_goals.append(learning_goal)

            if len(detected_goals) > 0:
                return detected_goals

        return []
