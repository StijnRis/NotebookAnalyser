from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from content_log.notebook_content.notebook_content import NotebookContent


class NotebookCell:
    @staticmethod
    def load(data: Dict[str, Any]):
        return NotebookCell(data.get("id"), data["index"])
    
    def __init__(self, id: Optional[str], index: int):
        self.id = id
        self.index = index

class NotebookKernelError:
    @staticmethod
    def load(data: Dict[str, Any]):
        return NotebookKernelError(
            data["errorName"],
            data["errorValue"],
            data["traceback"],
        )
    
    def __init__(self, errorName: str, errorValue: str, traceback: List[str]):
        self.errorName = errorName
        self.errorValue = errorValue
        self.traceback = traceback



@dataclass
class NotebookEventInfo:
    @staticmethod
    def load(data: Dict[str, Any]):
        cells = None
        if "cells" in data:
            cells = [NotebookCell.load(cell) for cell in data["cells"]]
        kernelError = None
        if kernelError in data:
            kernelError = NotebookKernelError.load(
                data["kernelError"],
            )

        return NotebookEventInfo(
            data.get("index"),
            data.get("doc"),
            data.get("changes"),
            cells,
            data.get("environ"),
            data.get("success"),
            kernelError,
            data.get("selection"),
        )

    index: Optional[int] = None
    doc: Optional[List[str]] = None
    changes: Optional[List[Union[int, List[Union[int, str]]]]] = None
    cells: Optional[List[NotebookCell]] = None
    environ: Optional[Dict[str, str]] = None
    success: Optional[bool] = None
    kernelError: Optional[NotebookKernelError] = None
    selection: Optional[str] = None

class NotebookEventName(Enum):
    NOTEBOOK_VISIBLE = "NotebookVisibleEvent"
    NOTEBOOK_HIDDEN = "NotebookHiddenEvent"
    NOTEBOOK_OPEN = "NotebookOpenEvent"
    CELL_EXECUTE = "CellExecuteEvent"
    CELL_EDIT = "CellEditEvent"
    ACTIVE_CELL_CHANGE = "ActiveCellChangeEvent"
    NOTEBOOK_SCROLL = "NotebookScrollEvent"
    CLIPBOARD_PASTE = "ClipboardPasteEvent"
    CLIPBOARD_COPY = "ClipboardCopyEvent"
    CELL_ADD = "CellAddEvent"
    CELL_REMOVE = "CellRemoveEvent"
    NOTEBOOK_SAVE = "NotebookSaveEvent"
    CLIPBOARD_CUT = "ClipboardCutEvent"

@dataclass
class NotebookEventDetail:
    @staticmethod
    def load(data: Any):
        eventInfo = None
        if data["eventInfo"] is not None:
            eventInfo = NotebookEventInfo.load(data["eventInfo"])

        seconds = data["eventTime"] / 1000
        eventTime = datetime.fromtimestamp(seconds)

        return NotebookEventDetail(
            NotebookEventName(data["eventName"]),
            eventTime,
            eventInfo,
        )
    
    def __init__(
        self,
        eventName: NotebookEventName,
        eventTime: datetime,
        eventInfo: Optional[NotebookEventInfo],
    ):
        self.eventName = eventName
        self.eventTime = eventTime



class NotebookState:
    @staticmethod
    def load(data: dict[str, Any]):
        notebookContent = None
        if "notebookContent" in data and data["notebookContent"] is not None:
            notebookContent = NotebookContent.load(data["notebookContent"])

        return NotebookState(
            data.get("sessionID"),
            data["notebookPath"],
            notebookContent,
        )

    def __init__(
        self,
        sessionID: Optional[str],
        notebookPath: str,
        notebookContent: Optional[NotebookContent],
    ):
        self.sessionID = sessionID
        self.notebookPath = notebookPath
        self.notebookContent = notebookContent


@dataclass
class NotebookLogEntry:
    @staticmethod
    def load(data: dict[str, Any]):
        eventDetail = NotebookEventDetail.load(data["eventDetail"])
        notebookState = NotebookState.load(data["notebookState"])

        return NotebookLogEntry(eventDetail, notebookState)

    eventDetail: NotebookEventDetail
    notebookState: NotebookState
