from matplotlib.testing import set_font_settings_for_testing
from activity.cell_activity import CellActivity
from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser
from chat_log.chat_activity import ChatActivity
from chat_log.chat_log import ChatLog
from notebook_log.notebook_log import NotebookLog


class User:
    def __init__(self, username: str, chat_log: ChatLog, notebook_log: NotebookLog, notebook_files: list[str]):
        self.username = username
        self.chat_log = chat_log
        self.notebook_log = notebook_log
        self.notebook_files = notebook_files

    def get_username(self):
        return self.username

    def get_chat_log(self):
        return self.chat_log

    def get_notebook_log(self):
        return self.notebook_log

    def get_notebook_files(self):
        return self.notebook_files

    # TODO fix
    def get_cell_activities(self) -> list[CellActivity]:
        activities: list[CellActivity] = []

        notebook_activities = self.notebook_log.get_notebook_cell_activity_composites()
        for notebook_activity in notebook_activities:
            messages = []
            users = {}
            for notebook_sub_activity in notebook_activity.cell_activities:
                activity = self.chat_log.get_activity_between(
                    notebook_sub_activity.get_start_time(),
                    notebook_sub_activity.get_end_time(),
                )
                messages.extend(activity.messages)
                users.update(activity.users)
            activities.append(
                CellActivity(notebook_activity, ChatActivity(messages, users))
            )

        return activities

    def get_event_sequence(self):
        """
        Get all (time, event_type) pairs of the notebook and the chat
        """

        sequence = self.notebook_log.get_event_sequence()
        sequence2 = self.chat_log.get_event_sequence()
        sequence.extend(sequence2)
        sequence.sort(key=lambda x: x[0])

        return sequence

    def get_overview(self, level=1):
        """
        Provide an overview of activities.
        """
        activities = "\n".join(
            [
                activity.get_overview(level + 1)
                for activity in self.get_cell_activities()
            ]
        )
        return (
            f"{'#' * level} Summary for user {self.username}\n\n"
            f"{self.chat_log.get_overview(level)}\n"
            f"{self.notebook_log.get_overview(level)}\n"
            f"{'#' * (level + 1)} Cell activities\n\n"
            f"{activities}"
        )

    def get_summary(self):
        return f"User {self.username}"
