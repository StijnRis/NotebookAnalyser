from abc import ABC
from datetime import datetime


class ContentEvent(ABC):
    def __init__(self, event_time: datetime):
        self.event_time = event_time
    
    def get_time(self) -> datetime:
        return self.event_time


class FileVisibleEvent(ContentEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileHiddenEvent(ContentEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileOpenEvent(ContentEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ExecuteEvent(ContentEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class EditEvent(ContentEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class ActiveCellChangeEvent(ContentEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class FileScrollEvent(ContentEvent):
    def __init__(self, eventTime: datetime, scrollPosition: int):
        super().__init__(eventTime)
        self.scrollPosition = scrollPosition

    def get_scroll_position(self) -> int:
        return self.scrollPosition


class ClipboardPasteEvent(ContentEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class ClipboardCopyEvent(ContentEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class CellAddEvent(ContentEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class CellRemoveEvent(ContentEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class FileSaveEvent(ContentEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ClipboardCutEvent(ContentEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content
