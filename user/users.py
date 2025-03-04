import os
import pickle

from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from user.user import User


class Users:

    @staticmethod
    def load_from_file(path: str):
        with open(path, "rb") as f:
            loaded_processor: Users = pickle.load(f)
            return loaded_processor

    def __init__(self, chat_message_analyser: ChatMessageAnalyser):
        self.users: list[User] = []
        self.chat_message_analyser = chat_message_analyser

    def save_to_file(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def get_users(self):
        return self.users
    
    def add_user(self, user: User):
        self.users.append(user)

    def get_user_by_name(self, username: str):
        for user in self.users:
            if user.get_username() == username:
                return user
        return None

    def get_summary(self):
        return "\n".join([user.get_summary() for user in self.users])
