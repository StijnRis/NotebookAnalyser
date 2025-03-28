from chatbot import Chatbot
from content_log.execution_log.analyser.execution_error_result_analyser import (
    ExecutionErrorResultAnalyser,
)
from content_log.execution_log.execution_result import ExecutionErrorResult
from processor.learning_goal import LearningGoal


class ChatbotExecutionErrorResultAnalyser(ExecutionErrorResultAnalyser):

    def __init__(self, error_types: list[LearningGoal], chatbot: Chatbot):
        super().__init__(error_types)
        self.chatbot = chatbot

    def get_error_type(self, error_event: "ExecutionErrorResult") -> "LearningGoal":
        learning_goals_string = "\n".join(
            [
                f"- {error_type.name}: {error_type.description}"
                for error_type in self.error_types
            ]
        )
        query = f"To which learning goal does this error belong? Choose from the following options: \n{learning_goals_string}\n\n Only answer the name of the chosen option. \n The error: \n\n {error_event.get_error_value()} \n\n {error_event.get_cleaned_traceback()}"
        response = self.chatbot.ask_question(query).lower().strip()
        for i in range(3):
            chosen_error_types = []
            for error_type in self.error_types:
                if error_type.name.lower() in response.lower():
                    chosen_error_types.append(error_type)

            if len(chosen_error_types) == 1:
                return chosen_error_types[0]

            # Try again
            response = self.chatbot.ask_question_without_cache(query)

        return LearningGoal("NOT_DETECTED", "The error type was not detected")
