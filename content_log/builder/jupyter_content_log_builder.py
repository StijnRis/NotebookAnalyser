import json
from datetime import datetime

from content_log.code.code_file import CodeFile
from content_log.code.file_versions_log import CodeVersionsLog
from content_log.code.source_code import SourceCode
from content_log.editing_log.editing_event import (
    ClipboardCopyEvent,
    ClipboardCutEvent,
    ClipboardPasteEvent,
    EditEvent,
    EditingEvent,
)
from content_log.editing_log.editing_file_log import EditingFileLog
from content_log.execution_log.execution_output import (
    EmptyResult,
    ErrorResult,
    ExecuteResult,
    ExecutionOutput,
    StreamResult,
)
from content_log.execution_log.file_execution_log import FileExecutionLog
from content_log.file_log import FileLog
from content_log.workspace_log import WorkspaceLog


class JupyterWorkspaceLogBuilder:
    def __init__(self):
        self.editing_events: dict[str, list[EditingEvent]] = {}
        self.execution_events: dict[str, list[ExecutionOutput]] = {}
        self.source_codes: dict[str, list[CodeFile]] = {}

    def load_files(self, file_paths: list[str]):
        for file_path in file_paths:
            self.load_file(file_path)

    def load_file(self, file_path: str):
        with open(file_path, "r", encoding="utf8") as file:
            data = file.read()
            data = "[" + data[:-1] + "]"
            data = json.loads(data)

        for event_data in data:
            self.load_editing_event(event_data)
            self.load_file_execution_event(event_data)
            self.load_code_files(event_data)

    def get_editing_info_for_file(self, file_path: str):
        if file_path not in self.editing_events:
            self.editing_events[file_path] = []
            self.execution_events[file_path] = []
            self.source_codes[file_path] = []

        return self.editing_events[file_path]

    def get_execution_info_for_file(self, file_path: str):
        if file_path not in self.execution_events:
            self.editing_events[file_path] = []
            self.execution_events[file_path] = []
            self.source_codes[file_path] = []

        return self.execution_events[file_path]

    def get_source_code_info_for_file(self, file_path: str):
        if file_path not in self.source_codes:
            self.editing_events[file_path] = []
            self.execution_events[file_path] = []
            self.source_codes[file_path] = []

        return self.source_codes[file_path]

    def load_editing_event(self, event_data: dict):
        event = self.parse_editing_event(event_data)

        if event is None:
            return

        log_entry, index = event
        file = event_data["notebookState"]["notebookPath"]
        file_name = f"{file}_{index}"

        file_info = self.get_editing_info_for_file(file_name)

        file_info.append(log_entry)

    def parse_editing_event(self, data: dict) -> tuple[EditingEvent, int] | None:
        event_type = data["eventDetail"]["eventName"]
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000)

        if event_type == "CellEditEvent":
            return EditEvent(event_time), data["eventDetail"]["eventInfo"]["index"]
        elif event_type == "NotebookVisibleEvent":
            pass
            # return FileVisibleEvent(event_time), None
        elif event_type == "NotebookHiddenEvent":
            pass
            # return FileHiddenEvent(event_time), None
        elif event_type == "NotebookOpenEvent":
            pass
            # return FileOpenEvent(event_time), None
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

    def load_file_execution_event(self, data: dict):
        events = self.parse_file_execution_events(data)

        if events is None:
            return

        file = data["notebookState"]["notebookPath"]
        index = data["eventDetail"]["eventInfo"]["cells"][0]["index"]
        file_name = f"{file}_{index}"

        file_info = self.get_execution_info_for_file(file_name)

        file_info.extend(events)

    def parse_file_execution_events(self, data: dict) -> list[ExecutionOutput] | None:
        event_type = data["eventDetail"]["eventName"]
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000)

        if event_type != "CellExecuteEvent":
            return

        notebook_state = data["notebookState"]
        assert notebook_state is not None, "Notebook state is missing"

        cells = notebook_state["notebookContent"]["cells"]

        executed_cell_index = data["eventDetail"]["eventInfo"]["cells"][0][
            "index"
        ]
        executed_cell = cells[executed_cell_index]

        if executed_cell["cell_type"] != "code":
            return

        outputs = executed_cell["outputs"]

        if len(outputs) == 0:
            return [EmptyResult(event_time)]


        events = []
        for output_data in outputs:
            if output_data["output_type"] == "stream":
                events.append(StreamResult(event_time, output_data["text"]))
            elif output_data["output_type"] == "error":
                events.append(
                    ErrorResult(
                        event_time,
                        output_data["traceback"],
                        output_data["ename"],
                        output_data["evalue"],
                    )
                )
            elif output_data["output_type"] == "execute_result":
                events.append(ExecuteResult(event_time, output_data["data"]))
            else:
                raise ValueError(f"Unknown output type: {output_data['output_type']}")

        return events

    def load_code_files(self, data: dict):
        if "notebookState" not in data or data["notebookState"]["notebookContent"] is None:
            return
        
        file_path = data["notebookState"]["notebookPath"]
        code_files = self.parse_code_files(data, file_path)

        for code_file in code_files:
            file_info = self.get_source_code_info_for_file(code_file.get_path())

            file_info.append(code_file)

    def parse_code_files(self, data: dict, file: str) -> list[CodeFile]:
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000)

        cells = data["notebookState"]["notebookContent"]["cells"]

        code_files = []
        for index, cell in enumerate(cells):
            if cell["cell_type"] == "code":
                code = cell["source"]
                source_code = CodeFile(event_time, code, f"{file}_{index}")

                code_files.append(source_code)

        return code_files

    def build(self) -> WorkspaceLog:
        file_logs = []

        for file in self.editing_events:
            editing_log = EditingFileLog(file, self.editing_events[file])
            file_execution_log = FileExecutionLog(self.execution_events[file])
            code_version_manager = CodeVersionsLog(self.source_codes[file])

            file_log = FileLog(
                file, editing_log, code_version_manager, file_execution_log
            )
            file_logs.append(file_log)

        workspace_log = WorkspaceLog(file_logs)
        return workspace_log
