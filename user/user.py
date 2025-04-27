from datetime import datetime

from activity.file_activity import FileActivity
from chat_log.chat_log import ChatLog
from content_log.workspace_log import WorkspaceLog


class User:
    def __init__(
        self,
        username: str,
        chat_log: ChatLog,
        workspace_log: WorkspaceLog,
        files: list[str],
    ):
        self.username = username
        self.chat_log = chat_log
        self.workspace_log = workspace_log
        self.files = files

    def get_username(self):
        return self.username

    def get_chat_log(self):
        return self.chat_log

    def get_workspace_log(self):
        return self.workspace_log

    def get_files(self):
        return self.files

    def get_file_activities(self) -> list[FileActivity]:
        activities: list[FileActivity] = []

        file_logs = self.workspace_log.get_file_logs()
        for file_log in file_logs:
            messages = []
            users = {}
            for (
                start_time,
                end_time,
            ) in file_log.get_editing_log().get_editing_periods():
                activity = self.chat_log.get_activity_between(
                    start_time,
                    end_time,
                )
                messages.extend(activity.messages)
            activities.append(FileActivity(file_log, ChatLog(messages)))

        return activities

    def get_event_sequence(self):
        """
        Get all (time, event_type) pairs of the files and the chat
        """

        sequence: list[tuple[datetime, str]] = []
        sequence1 = self.workspace_log.get_event_sequence()
        sequence.extend(sequence1)
        sequence2 = self.chat_log.get_event_sequence()
        sequence.extend(sequence2)
        sequence.sort(key=lambda x: x[0])

        return sequence
