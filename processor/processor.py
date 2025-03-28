from dotenv import load_dotenv

from analyser.analyser import Analyser
from analyser.code_file_analyser import CodeFileAnalyser
from analyser.event_sequence_analysis import EventSequenceAnalysis
from analyser.file_activity_analyser import FileActivityAnalyser
from analyser.interaction_analyser import InteractionAnalyser
from analyser.question_analyser import QuestionAnalyser
from analyser.runtime_error_analyser import RunTimeAnalyser
from analyser.user_analyser import UserAnalyser
from chat_log.analyser.chatbot_chat_message_analyser import ChatbotChatMessageAnalyser
from chatbot import Chatbot
from report.report_generator import ReportGenerator
from user.builder.jupyter_users_builder import JupyterUsersBuilder


class Processor:
    def __init__(self):
        load_dotenv()

        self.chatbot_cache = "output/chatbot_cache.json"
        self.chatbot = Chatbot(self.chatbot_cache)

        self.chat_message_analyser = ChatbotChatMessageAnalyser(self.chatbot)

        self.analysers: list[Analyser] = [
            # UserAnalyser(),
            # CodeFileAnalyser(),
            # EventSequenceAnalysis(),
            # FileActivityAnalyser(),
            # QuestionAnalyser(),
            # InteractionAnalyser(),
            RunTimeAnalyser(),
        ]

        self.load_users()

    def load_users(self):
        small_sample_data_location = [
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\logs",
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\volumes",
        ]

        all_data_location = [
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\logs",
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\volumes",
        ]

        data_location = small_sample_data_location

        builder = JupyterUsersBuilder(self.chat_message_analyser, verbose=True)
        builder.load_log_directory(data_location[0])
        builder.load_volumes_directory(data_location[1])
        self.users = builder.build()

    def run(self):
        file_path = "output/users_analyser.xlsx"
        report_generator = ReportGenerator(file_path)

        # Analyze users
        amount_of_users = len(self.users.get_users())
        for index, user in enumerate(self.users.get_users(), start=1):
            print(f"Processing user {user.username} ({index}/{amount_of_users})")
            for analyser in self.analysers:
                # try:
                analyser.analyse_user(user)
                # except Exception as e:
                #     print(f"Error processing user {user.username}: {e}")

        # print("Analyzing event sequences")
        # event_sequence_analyser = EventSequenceAnalysis(self.users)
        # event_sequence_analyser.generate_report()

        print("Generating report")
        for analyser in self.analysers:
            analyser.save_result_to_report(report_generator)

        report_generator.close()

        print("Analysis completed.")
