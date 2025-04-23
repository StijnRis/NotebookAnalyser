import os
from datetime import datetime

from analyser.analyser import Analyser
from analyser.code_file_analyser import CodeFileAnalyser
from analyser.execution_analyser import ExecutionAnalyser
from analyser.file_activity_analyser import FileActivityAnalyser
from analyser.interaction_analyser import InteractionAnalyser
from analyser.learning_goals_analyser import LearningGoalsAnalyser
from analyser.question_analyser import QuestionAnalyser
from analyser.user_analyser import UserAnalyser
from chat_log.analyser.chatbot_chat_message_analyser import ChatbotChatMessageAnalyser
from chatbot import Chatbot
from content_log.execution_log.analyser.chatbot_execution_error_result_analyser import (
    ChatbotExecutionErrorResultAnalyser,
)
from processor.learning_goal.for_loop_learning_goal import ForLoopLearningGoal
from processor.learning_goal.function_call_learning_goal import FunctionCallLearningGoal
from processor.learning_goal.function_definition_learning_goal import (
    FunctionDefinitionLearningGoal,
)
from processor.learning_goal.if_statement_learning_goal import IfStatementLearningGoal
from processor.learning_goal.import_statement_learning_goal import (
    ImportStatementLearningGoal,
)
from processor.learning_goal.list_access_learning_goal import ListAccessLearningGoal
from processor.learning_goal.list_assignment_learning_goal import (
    ListAssignmentLearningGoal,
)
from processor.learning_goal.list_declaration_learning_goal import (
    ListDeclarationLearningGoal,
)
from processor.learning_goal.print_statement_learning_goal import (
    PrintStatementLearningGoal,
)
from processor.learning_goal.type_casting_learning_goal import TypeCastingLearningGoal
from processor.learning_goal.variable_assignment_learning_goal import (
    VariableAssignmentLearningGoal,
)
from processor.learning_goal.while_loop_learning_goal import WhileLoopLearningGoal
from report.report_generator import ReportGenerator
from user.builder.jupyter_users_builder import JupyterUsersBuilder


class Processor:
    def __init__(self):
        self.chatbot_cache = "output/chatbot_cache.json"
        self.chatbot = Chatbot(self.chatbot_cache)

        self.chat_message_analyser = ChatbotChatMessageAnalyser(self.chatbot)

        self.learning_goals = [
            VariableAssignmentLearningGoal(),
            IfStatementLearningGoal(),
            ForLoopLearningGoal(),
            WhileLoopLearningGoal(),
            FunctionDefinitionLearningGoal(),
            FunctionCallLearningGoal(),
            ListDeclarationLearningGoal(),
            ListAccessLearningGoal(),
            ListAssignmentLearningGoal(),
            ImportStatementLearningGoal(),
            TypeCastingLearningGoal(),
            PrintStatementLearningGoal(),
        ]

        self.execution_error_result_analyser = ChatbotExecutionErrorResultAnalyser(
            self.learning_goals, self.chatbot
        )

        self.analysers: list[Analyser] = [
            UserAnalyser(),
            CodeFileAnalyser(),
            # EventSequenceAnalysis(),
            FileActivityAnalyser(),
            QuestionAnalyser(),
            InteractionAnalyser(),
            ExecutionAnalyser(self.learning_goals),
            LearningGoalsAnalyser(self.learning_goals),
        ]

        self.load_users()

    def load_users(self):
        local_data_location = {
            "logs": [
                r"C:\University\Honours\Data (temp)\All data with consent\logs from around 2025-03-13 until 2025-04-22",
                r"C:\University\Honours\Data (temp)\All data with consent\logs from start until 2025-03-09",
            ],
            "volumes": [
                r"C:\University\Honours\Data (temp)\All data with consent\volumes",
            ],
        }

        small_sample_data_location = [
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\logs",
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Small_sample_of_data\volumes",
        ]

        all_data_location = [
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\logs",
            r"W:\staff-umbrella\DataStorageJELAI\StanislasExperimentData\Backup_2025_02_26\volumes",
        ]

        data_location = local_data_location

        builder = JupyterUsersBuilder(
            self.chat_message_analyser, self.execution_error_result_analyser
        )

        username = os.getenv("FILTER_USERNAME")
        if username:
            builder.apply_user_filter(username)

        for log_dir in data_location["logs"]:
            builder.load_log_directory(log_dir)
        for volume_dir in data_location["volumes"]:
            builder.load_volumes_directory(volume_dir)
        self.users = builder.build()

    def run(self):
        current_date = datetime.now().strftime("%Y_%m_%d")
        file_path = f"output/analyses_{current_date}.xlsx"
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

        print("Generating report")
        for analyser in self.analysers:
            analyser.save_result_to_report(report_generator)

        report_generator.close()

        print(f"Report saved to {file_path}")
        print("Analysis completed.")
