from abc import ABC, abstractmethod
from typing import List

from chat_log.chat_log import ChatLog


class ChatLogBuilder(ABC):
    @abstractmethod
    def load_files(self, file_paths: List[str]) -> None:
        pass

    @abstractmethod
    def load_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def build(self) -> ChatLog:
        pass
