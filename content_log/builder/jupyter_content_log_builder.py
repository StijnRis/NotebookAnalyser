import json
from datetime import datetime

from editing_log.editing_event import (
    ClipboardCopyEvent,
    ClipboardCutEvent,
    ClipboardPasteEvent,
    EditEvent,
    EditingEvent,
    FileHiddenEvent,
    FileOpenEvent,
    FileVisibleEvent,
)

from content_log.editing_log.editing_code_snippet_log import EditingCodeSnippetLog
from content_log.editing_log.editing_notebook_log import EditingNotebookLog
from content_log.notebook_log import NotebookLog


class JupyterContentLogBuilder:
    def __init__(self):
        self.code_snippet_events: dict[str, dict[int, list[EditingEvent]]] = {}
        self.file_events: dict[str, list[EditingEvent]] = {}

    def load_files(self, file_paths: list[str]):
        for file_path in file_paths:
            self.load_file(file_path)

    def load_file(self, file_path: str):
        with open(file_path, "r", encoding="utf8") as file:
            data = file.read()
            data = "[" + data[:-1] + "]"
            data = json.loads(data)

        for event_data in data:
            event = self.parse_event(event_data)

            if event is None:
                continue

            log_entry, index = event

            file = event_data["notebookState"]["notebookPath"]
            if file not in self.code_snippet_events:
                self.code_snippet_events[file] = {}

            if file not in self.file_events:
                self.file_events[file] = []

            self.file_events[file].append(log_entry)

            if index is not None:
                if index not in self.code_snippet_events[file]:
                    self.code_snippet_events[file][index] = []

                self.code_snippet_events[file][index].append(log_entry)

    def parse_event(self, data: dict) -> tuple[EditingEvent, int | None] | None:
        event_type = data["eventDetail"]["eventName"]
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"])

        if event_type == "CellEditEvent":
            return EditEvent(event_time), data["eventDetail"]["eventInfo"]["index"]
        elif event_type == "NotebookVisibleEvent":
            return FileVisibleEvent(event_time), None
        elif event_type == "NotebookHiddenEvent":
            return FileHiddenEvent(event_time), None
        elif event_type == "NotebookOpenEvent":
            return FileOpenEvent(event_time), None
        elif event_type == "CellExecuteEvent":
            pass
            # return ExecuteEvent(event_time), None
        elif event_type == "ActiveCellChangeEvent":
            pass
            # return ActiveCellChangeEvent(event_time, data["eventDetail"]["eventInfo"]["cellId"]), None
        elif event_type == "NotebookScrollEvent":
            pass
            # return FileScrollEvent(event_time), None
        elif event_type == "ClipboardPasteEvent":
            return (
                ClipboardPasteEvent(
                    event_time, data["eventDetail"]["eventInfo"]["selection"]
                ),
                data["eventDetail"]["eventInfo"]["cells"][0]["index"],
            )
        elif event_type == "ClipboardCopyEvent":
            return (
                ClipboardCopyEvent(
                    event_time, data["eventDetail"]["eventInfo"]["selection"]
                ),
                data["eventDetail"]["eventInfo"]["cells"][0]["index"],
            )
        elif event_type == "ClipboardCutEvent":
            return (
                ClipboardCutEvent(
                    event_time, data["eventDetail"]["eventInfo"]["selection"]
                ),
                data["eventDetail"]["eventInfo"]["cells"][0]["index"],
            )
        elif event_type == "CellAddEvent":
            pass
            # return CellAddEvent(event_time), None
        elif event_type == "CellRemoveEvent":
            pass
            # return CellRemoveEvent(event_time), None
        elif event_type == "NotebookSaveEvent":
            pass
            # return FileSaveEvent(event_time), None
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        return None

    def build(self):
        editing_notebook_logs = []

        for file, events in self.file_events.items():
            editing_code_snippet_logs = []

            for index, events in self.code_snippet_events[file].items():
                editing_code_snippet_logs.append(EditingCodeSnippetLog(events))

            editing_notebook_log = EditingNotebookLog(
                file, events, editing_code_snippet_logs
            )
            file_log = NotebookLog(editing_notebook_log, execution_log)
            editing_notebook_logs.append(editing_notebook_log)

        return editing_notebook_logs
