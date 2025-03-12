import pickle

from user.user import User


class Users:

    def __init__(self, users: list[User]):
        self.users: list[User] = users

    def get_users(self):
        return self.users

    def get_user_by_name(self, username: str):
        for user in self.users:
            if user.get_username() == username:
                return user
        return None

    def get_summary(self):
        return "\n".join([user.get_summary() for user in self.users])
