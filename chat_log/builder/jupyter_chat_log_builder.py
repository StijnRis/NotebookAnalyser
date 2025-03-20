import json
from typing import Any

from chat_log.builder.chat_log_builder import ChatLogBuilder
from chat_log.chat_log import ChatLog
from chat_log.chat_message import ChatMessage
from chat_log.chat_user import ChatUser


class JupyterChatLogBuilder(ChatLogBuilder):
    def __init__(self, chat_message_analyser):
        self.chat_message_analyser = chat_message_analyser
        self.messages = []
        self.users = {}

    def load_chat_files(self, file_paths: list[str]):
        for file_path in file_paths:
            self.load_chat_file(file_path)

    def load_chat_file(self, file_path: str):
        with open(file_path, "r") as file:
            if file.read(1) == "":
                return []
            else:
                file.seek(0)
                data = json.load(file)

        self.load(data)

    def load(self, data: dict[str, Any]):
        messages = [
            ChatMessage(**msg, chat_message_analyser=self.chat_message_analyser)
            for msg in data["messages"]
        ]
        users = {key: ChatUser(**value) for key, value in data["users"].items()}
        self.messages.extend(messages)
        self.users.update(users)
        # datetime.fromtimestamp(time)
        if self.automated == True:
            return False
        if self.sender == "Juno":
            return False
        return True

    def build(self):
        chat_log = ChatLog(self.messages, self.users, self.chat_message_analyser)

        self.messages = []
        self.users = {}

        return chat_log
