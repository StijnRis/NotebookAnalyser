import json
from notebook_log.notebook_log import NotebookLog
from notebook_log.entry.notebook_log_entry import NotebookLogEntry


class NotebookLogBuilder():
    def __init__(self):
        self.all_log_entries = []

    def load_files(self, file_paths: list[str]):
        for file_path in file_paths:
            self.load_file(file_path)

    def load_file(self, file_path: str):
        with open(file_path, "r", encoding="utf8") as file:
            data = file.read()
            data = "[" + data[:-1] + "]"
            data = json.loads(data)

        log_entries = [NotebookLogEntry.load(entry) for entry in data]
        self.all_log_entries.extend(log_entries)
    
    def build(self):
        notebook_log = NotebookLog(self.all_log_entries)

        self.all_log_entries = []

        return notebook_log

    
