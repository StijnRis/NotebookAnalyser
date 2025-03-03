import os

from dotenv import load_dotenv

from chat_log.analyser.chatbot_chat_message_analyser import ChatbotChatMessageAnalyser
from chatbot import Chatbot
from processor.questions_analyser import QuestionsAnalyser
from processor.report_generator import ReportGenerator
from processor.users_notebooks_analyser import UsersNotebooksAnalyser
from user.users import Users
from user.users_builder import UsersBuilder


class Processor:
    def __init__(self):
        load_dotenv()

        self.chatbot_cache = "output/chatbot_cache.json"
        self.chatbot = Chatbot()
        self.chatbot.load_cache(self.chatbot_cache)

        self.chat_message_analyser = ChatbotChatMessageAnalyser(self.chatbot)

        self.users_cache = "output/users.pkl"

        self.load_users()

    def load_users(self):
        # Check if we use cache
        cache_exists = os.path.exists(self.users_cache)
        user_input = None
        if cache_exists:
            user_input = input("Use cache (y/n)? ")

        if cache_exists and user_input == "y":
            print("Loading users from saved file")
            self.users = Users.load_from_file(
                self.users_cache, self.chat_message_analyser
            )
        else:
            builder = UsersBuilder(verbose=True)
            builder.load_log_directory(
                r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\logs"
            )
            builder.load_volumes_directory(
                r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\volumes"
            )
            self.users = builder.build(self.chat_message_analyser)
            self.users.save_to_file(self.users_cache)

    def run(self):
        file_path = "output/users_analyser.xlsx"
        report_generator = ReportGenerator(file_path)

        print("Analyzing questions")
        questions_analyser = QuestionsAnalyser(report_generator)
        questions_analyser.analyse_users(self.users)
        questions_analyser.save_result_to_report(report_generator)

        # print("Analyzing event sequences")
        # event_sequence_analyser = EventSequenceAnalysis(self.users)
        # event_sequence_analyser.generate_report()

        print("Analyzing users")

        notebook_analyser = UsersNotebooksAnalyser()
        notebook_analyser.analyse_users(self.users)
        notebook_analyser.save_result_to_report(report_generator)

        print("Closing")
        report_generator.close()
        self.stop()

        print("Analysis completed.")

    def stop(self):
        self.chatbot.save_cache(self.chatbot_cache)
