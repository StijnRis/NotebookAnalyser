from abc import ABC
from datetime import datetime

class EditingEvent(ABC):
    def __init__(self, event_time: datetime):
        self.event_time = event_time

    def get_time(self) -> datetime:
        return self.event_time


class FileVisibleEvent(EditingEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileHiddenEvent(EditingEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileOpenEvent(EditingEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ExecuteEvent(EditingEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class EditEvent(EditingEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ActiveCellChangeEvent(EditingEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class FileScrollEvent(EditingEvent):
    def __init__(self, eventTime: datetime, scrollPosition: int):
        super().__init__(eventTime)
        self.scrollPosition = scrollPosition

    def get_scroll_position(self) -> int:
        return self.scrollPosition


class ClipboardPasteEvent(EditingEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class ClipboardCopyEvent(EditingEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class CellAddEvent(EditingEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class CellRemoveEvent(EditingEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class FileSaveEvent(EditingEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ClipboardCutEvent(EditingEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content
