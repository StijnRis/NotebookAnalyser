from datetime import datetime
from activity.file_activity import FileActivity
from chat_log.chat_activity import ChatActivity
from chat_log.chat_log import ChatLog
from notebook_log.notebook_log import NotebookLog
from notebook_log.notebook_log_entry import NotebookEventName


class User:
    def __init__(
        self,
        username: str,
        chat_log: ChatLog,
        notebook_log: NotebookLog,
        notebook_files: list[str],
    ):
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

    def get_file_activities(self):
        activities: list[FileActivity] = []

        notebook_file_activities = self.notebook_log.split_by_file()
        for notebook_activity in notebook_file_activities:
            messages = []
            users = {}
            for start_time, end_time in notebook_activity.get_visible_periods():
                activity = self.chat_log.get_activity_between(
                    start_time,
                    end_time,
                )
                messages.extend(activity.messages)
                users.update(activity.users)
            activities.append(
                FileActivity(notebook_activity, ChatActivity(messages, users))
            )

        return activities

    def get_event_sequence(self):
        """
        Get all (time, event_type) pairs of the notebook and the chat
        """

        sequence: list[tuple[datetime, str]] = []
        sequence1 = self.notebook_log.get_event_sequence()
        sequence.extend([(time, event_name.value) for time, event_name in sequence1])
        sequence2 = self.chat_log.get_event_sequence()
        sequence.extend(sequence2)
        sequence.sort(key=lambda x: x[0])

        return sequence
