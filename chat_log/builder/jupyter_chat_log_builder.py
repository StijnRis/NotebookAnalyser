import json
from datetime import datetime
from typing import Any

from chat_log.builder.chat_log_builder import ChatLogBuilder
from chat_log.chat_log import ChatLog
from chat_log.chat_message_answer import ChatMessageAnswer
from chat_log.chat_message_question import ChatMessageQuestion


class JupyterChatLogBuilder(ChatLogBuilder):
    def __init__(self, chat_message_analyser):
        self.chat_message_analyser = chat_message_analyser
        self.messages = []

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
        messages = []
        for msg in data["messages"]:
            time = datetime.fromtimestamp(msg["time"])
            body = msg["body"]
            automated = msg["automated"]
            if automated:
                messages.append(
                    ChatMessageAnswer(time, body, self.chat_message_analyser)
                )
            else:
                messages.append(
                    ChatMessageQuestion(time, body, self.chat_message_analyser)
                )

        self.messages.extend(messages)

    def build(self):
        chat_log = ChatLog(self.messages, self.chat_message_analyser)

        self.messages = []

        return chat_log
