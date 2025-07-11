import json
from datetime import datetime

from content_log.code_versions_log.code_file import CodeFile
from content_log.code_versions_log.code_versions_log import CodeVersionsLog
from content_log.event_log.content_event import (
    ClipboardCopyEvent,
    ClipboardCutEvent,
    ClipboardPasteEvent,
    ContentEvent,
    FileEditEvent,
)
from content_log.event_log.file_events_log import EditingFileLog
from content_log.execution_log.analyser.execution_error_result_analyser import (
    ExecutionErrorResultAnalyser,
)
from content_log.execution_log.execution_result import (
    ExecutionCompositeResult,
    ExecutionErrorResult,
    ExecutionStreamResult,
    ExecutionTextResult,
)
from content_log.execution_log.file_execution_log import FileExecutionLog
from content_log.file_log import FileLog
from content_log.workspace_log import WorkspaceLog


class JupyterWorkspaceLogBuilder:
    def __init__(self, execution_error_result_analyser: ExecutionErrorResultAnalyser):
        self.editing_events: dict[str, list[ContentEvent]] = {}
        self.execution_events: dict[str, list[ExecutionCompositeResult]] = {}
        self.source_codes: dict[str, list[CodeFile]] = {}
        self.execution_error_result_analyser = execution_error_result_analyser

    def reset(self):
        self.editing_events = {}
        self.execution_events = {}
        self.source_codes = {}

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

        log_entry, indexes = event
        file = event_data["notebookState"]["notebookPath"]

        for index in indexes:
            file_name = f"{file}_{index}"

            file_info = self.get_editing_info_for_file(file_name)

            file_info.append(log_entry)

    def parse_editing_event(self, data: dict) -> tuple[ContentEvent, list[int]] | None:
        event_type = data["eventDetail"]["eventName"]
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000)

        if event_type == "CellEditEvent":
            return FileEditEvent(event_time), [
                data["eventDetail"]["eventInfo"]["index"]
            ]
        elif event_type == "NotebookVisibleEvent":
            pass
            # return FileVisibleEvent(event_time), [cell["index"] for cell in data["eventDetail"]["eventInfo"]["cells"]]
        elif event_type == "NotebookHiddenEvent":
            pass
            # return FileHiddenEvent(event_time), [cell["index"] for cell in data["eventDetail"]["eventInfo"]["cells"]]
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
                [data["eventDetail"]["eventInfo"]["cells"][0]["index"]],
            )
        elif event_type == "ClipboardCopyEvent":
            return (
                ClipboardCopyEvent(
                    event_time, data["eventDetail"]["eventInfo"]["selection"]
                ),
                [data["eventDetail"]["eventInfo"]["cells"][0]["index"]],
            )
        elif event_type == "ClipboardCutEvent":
            return (
                ClipboardCutEvent(
                    event_time, data["eventDetail"]["eventInfo"]["selection"]
                ),
                [data["eventDetail"]["eventInfo"]["cells"][0]["index"]],
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

        file_info.append(events)

    def parse_file_execution_events(
        self, data: dict
    ) -> ExecutionCompositeResult | None:
        event_type = data["eventDetail"]["eventName"]
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000)

        if event_type != "CellExecuteEvent":
            return

        notebook_state = data["notebookState"]
        assert notebook_state is not None, "Notebook state is missing"

        cells = notebook_state["notebookContent"]["cells"]

        executed_cell_index = data["eventDetail"]["eventInfo"]["cells"][0]["index"]
        executed_cell = cells[executed_cell_index]

        if executed_cell["cell_type"] != "code":
            return

        outputs = executed_cell["outputs"]

        results = []
        for output_data in outputs:
            if output_data["output_type"] == "stream":
                results.append(ExecutionStreamResult(event_time, output_data["text"]))
            elif output_data["output_type"] == "error":
                results.append(
                    ExecutionErrorResult(
                        event_time,
                        "\n".join(output_data["traceback"]),
                        output_data["ename"],
                        output_data["evalue"],
                        self.execution_error_result_analyser,
                    )
                )
            elif output_data["output_type"] == "execute_result":
                results.append(ExecutionTextResult(event_time, output_data["data"]))
            else:
                raise ValueError(f"Unknown output type: {output_data['output_type']}")

        return ExecutionCompositeResult(event_time, results)

    def load_code_files(self, data: dict):
        if (
            "notebookState" not in data
            or "notebookContent" not in data["notebookState"]
            or data["notebookState"]["notebookContent"] is None
        ):
            return

        file_path = data["notebookState"]["notebookPath"]
        code_files = self.parse_code_files(data, file_path)

        for code_file in code_files:
            file_info = self.get_source_code_info_for_file(code_file.get_path())

            file_info.append(code_file)

    def parse_code_files(self, data: dict, file: str) -> list[CodeFile]:
        event_time = datetime.fromtimestamp(data["eventDetail"]["eventTime"] / 1000.0)

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
            code_version_manager = CodeVersionsLog(
                self.source_codes[file]
            ).remove_duplicates()

            file_log = FileLog(
                file, editing_log, code_version_manager, file_execution_log
            )
            file_logs.append(file_log)

        workspace_log = WorkspaceLog(file_logs)

        self.reset()

        return workspace_log
