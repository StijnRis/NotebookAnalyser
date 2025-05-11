from chatbot import Chatbot
from content_log.code_versions_log import code_file
from content_log.code_versions_log.code_file import CodeFile
from content_log.code_versions_log.code_versions_log import CodeVersionsLog
from content_log.execution_log.analyser.execution_error_result_analyser import (
    ExecutionErrorResultAnalyser,
)
from content_log.execution_log.execution_result import ExecutionErrorResult
from processor.learning_goal.learning_goal import LearningGoal


class ChatbotExecutionErrorResultAnalyser(ExecutionErrorResultAnalyser):

    def __init__(self, learning_goals: list[LearningGoal], chatbot: Chatbot):
        super().__init__(learning_goals)
        self.chatbot = chatbot

    def get_error_type(self, error_event: "ExecutionErrorResult", code_file: CodeFile) -> "LearningGoal":
        learning_goals_string = "\n".join(
            [
                f"- {error_type.name}: {error_type.description}"
                for error_type in self.learning_goals
            ]
        )
        query = f"You are an instructor that classifies mistakes. You first reason about them and then give your final verdict on the last line. Structure the last line as following: 'The learning goal is [name of learning goal]'. Classify the following error into one of the following learning goals: \n{learning_goals_string}\n\n Code: \n {code_file.get_code()}. \n\n Error: \n {error_event.get_error_value()} \n {error_event.get_cleaned_traceback()}"
        for i in range(5):
            if i == 0:
                response = self.chatbot.ask_question(query).lower().strip()
            else:
                response = self.chatbot.ask_question_without_cache(query).lower().strip()

            chosen_error_types = []
            last_sentence = response.split("\n")[-1]
            for learning_goal in self.learning_goals:
                if learning_goal.name.lower() in last_sentence:
                    chosen_error_types.append(learning_goal)

            if len(chosen_error_types) == 1:
                return chosen_error_types[0]


        raise ValueError(
            f"Could not find the error type in the response: {response}"
        )
