import os

from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.builder.jupyter_chat_log_builder import JupyterChatLogBuilder
from content_log.builder.jupyter_content_log_builder import JupyterWorkspaceLogBuilder
from content_log.execution_log.analyser.execution_error_result_analyser import (
    ExecutionErrorResultAnalyser,
)
from user.user import User
from user.users import Users


class JupyterUsersBuilder:

    def __init__(
        self,
        chat_message_analyser: ChatMessageAnalyser,
        execution_error_result_analyser: ExecutionErrorResultAnalyser,
        verbose: bool = False,
    ):
        self.users_data = {}
        self.chat_message_analyser = chat_message_analyser
        self.execution_error_result_analyser = execution_error_result_analyser
        self.verbose = verbose
        self.workspace_log_builder = JupyterWorkspaceLogBuilder(
            self.execution_error_result_analyser
        )
        self.chat_log_builder = JupyterChatLogBuilder(self.chat_message_analyser)

    def get_user_data(self, username: str):
        if username not in self.users_data:
            self.users_data[username] = {
                "chat_log_file_paths": [],
                "notebook_log_file_paths": [],
                "notebook_file_paths": [],
            }
        return self.users_data[username]

    def load_log_directory(self, log_directory: str):
        if self.verbose:
            print("Loading users from directory")

        # Extract all notebook logs
        for file_name in os.listdir(log_directory):
            path = os.path.join(log_directory, file_name)
            valid_file = file_name.startswith("jupyter-") and file_name.endswith("-log")

            if os.path.isfile(path) and valid_file:
                # Add notebook log file path to user
                username = file_name.replace("jupyter-", "").replace("-log", "")
                user_data = self.get_user_data(username)
                user_data["notebook_log_file_paths"].append(path)

    def load_volumes_directory(self, volumes_directory: str):

        if self.verbose:
            print("Finding users in volumes directory")

        # Extract all chat logs and notebooks
        for folder_name in os.listdir(volumes_directory):
            path = os.path.join(volumes_directory, folder_name)
            if os.path.isdir(path) and not folder_name.startswith("_"):
                username = folder_name

                if self.verbose:
                    print(f"Finding data of user {username}")

                user_data = self.get_user_data(username)
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        if file_name.endswith(".ipynb"):
                            user_data["notebook_file_paths"].append(file_path)
                        elif file_name.endswith(".chat"):
                            user_data["chat_log_file_paths"].append(file_path)

                self.users_data[username] = user_data

    def load_grades(self):
        pass

    def build(self):
        users = []

        # Load data into objects
        for username, user_data in self.users_data.items():
            if self.verbose:
                print(f"Loading user {username}: ")
                print(f"  {len(user_data['chat_log_file_paths'])} chat log files")
                print(
                    f"  {len(user_data['notebook_log_file_paths'])} notebook log files"
                )
                print(f"  {len(user_data['notebook_file_paths'])} notebook files")

            self.workspace_log_builder.load_files(user_data["notebook_log_file_paths"])
            workspace_log = self.workspace_log_builder.build()

            notebook_files = user_data["notebook_file_paths"]

            self.chat_log_builder.load_files(user_data["chat_log_file_paths"])
            chat_log = self.chat_log_builder.build()

            user = User(username, chat_log, workspace_log, notebook_files)

            users.append(user)

        self.users_data = {}

        return Users(users)
