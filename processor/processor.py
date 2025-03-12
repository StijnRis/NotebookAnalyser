from dotenv import load_dotenv

from chat_log.analyser.chatbot_chat_message_analyser import ChatbotChatMessageAnalyser
from chatbot import Chatbot
from processor.interaction_analyser import InteractionAnalyser
from processor.question_analyser import QuestionAnalyser
from processor.user_analyser import UserAnalyser
from processor.user_notebooks_analyser import NotebookAnalyser
from report.report_generator import ReportGenerator
from user.users_builder import UsersBuilder


class Processor:
    def __init__(self):
        load_dotenv()

        self.chatbot_cache = "output/chatbot_cache.json"
        self.chatbot = Chatbot(self.chatbot_cache)

        self.chat_message_analyser = ChatbotChatMessageAnalyser(self.chatbot)

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

        builder = UsersBuilder(self.chat_message_analyser, verbose=True)
        builder.load_log_directory(data_location[0])
        builder.load_volumes_directory(data_location[1])
        self.users = builder.build()

    def run(self):
        file_path = "output/users_analyser.xlsx"
        report_generator = ReportGenerator(file_path)

        # Setup analysers
        questions_analyser = QuestionAnalyser()
        interaction_analyser = InteractionAnalyser()
        notebook_analyser = NotebookAnalyser()
        user_analyser = UserAnalyser()

        # Analyze users
        amount_of_users = len(self.users.get_users())
        for index, user in enumerate(self.users.get_users(), start=1):
            print(f"Processing user {user.username} ({index}/{amount_of_users})")
            # try:
            questions_analyser.analyse_messages_of_user(user)
            interaction_analyser.analyse_interactions_of_user(user)
            notebook_analyser.analyse_notebooks_of_user(user)
            user_analyser.analyse_user(user)
            # except Exception as e:
            #     print(f"Error processing user {user.username}: {e}")

        # print("Analyzing event sequences")
        # event_sequence_analyser = EventSequenceAnalysis(self.users)
        # event_sequence_analyser.generate_report()

        print("Generating report")
        questions_analyser.save_result_to_report(report_generator)
        interaction_analyser.save_result_to_report(report_generator)
        notebook_analyser.save_result_to_report(report_generator)
        user_analyser.save_result_to_report(report_generator)
        report_generator.close()

        print("Analysis completed.")
