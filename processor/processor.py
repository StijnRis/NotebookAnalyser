import os

from dotenv import load_dotenv

from chat_log.analyser.chatbot_chat_message_analyser import ChatbotChatMessageAnalyser
from chatbot import Chatbot
from processor.interaction_analyser import InteractionAnalyser
from processor.question_analyser import QuestionAnalyser
from processor.user_analyser import UserAnalyser
from processor.user_notebooks_analyser import NotebookAnalyser
from report.report_generator import ReportGenerator
from user.users import Users
from user.users_builder import UsersBuilder


class Processor:
    def __init__(self):
        load_dotenv()

        self.chatbot_cache = "output/chatbot_cache.json"
        self.chatbot = Chatbot(self.chatbot_cache)

        self.chat_message_analyser = ChatbotChatMessageAnalyser(self.chatbot)

        self.users_cache = "output/users.pkl"

        self.load_users()

    def load_users(self):
        builder = UsersBuilder(verbose=True)
        builder.load_log_directory(
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\logs"
        )
        builder.load_volumes_directory(
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\volumes"
        )
        self.users = builder.build(self.chat_message_analyser)
        self.users.save_to_file(self.users_cache)

    def run(self):
        file_path = "output/users_analyser.xlsx"
        report_generator = ReportGenerator(file_path)

        print("Analyzing questions")
        questions_analyser = QuestionAnalyser()
        questions_analyser.analyse_messages_of_users(self.users)
        questions_analyser.save_result_to_report(report_generator)

        print("Analyzing interactions")
        interaction_analyser = InteractionAnalyser()
        interaction_analyser.analyse_interactions_of_users(self.users)
        interaction_analyser.save_result_to_report(report_generator)

        # print("Analyzing event sequences")
        # event_sequence_analyser = EventSequenceAnalysis(self.users)
        # event_sequence_analyser.generate_report()

        print("Analyzing notebooks")
        notebook_analyser = NotebookAnalyser()
        notebook_analyser.analyse_notebooks_of_users(self.users)
        notebook_analyser.save_result_to_report(report_generator)

        print("Analyzing users")
        user_analyser = UserAnalyser()
        user_analyser.analyse_users(self.users)
        user_analyser.save_result_to_report(report_generator)

        print("Generating report")
        report_generator.close()

        print("Analysis completed.")

