from abc import ABC
from datetime import datetime


class ContentEvent(ABC):
    def __init__(self, event_time: datetime):
        self.event_time = event_time

    def get_time(self) -> datetime:
        return self.event_time


class ContentPassiveEvent(ContentEvent, ABC):
    """
    An event that represent some passive action
    """


class FileOpenEvent(ContentPassiveEvent):
    """
    An event that represents the opening of a file
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileCloseEvent(ContentPassiveEvent):
    """
    An event that represents the closing of a file
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileVisibleEvent(ContentPassiveEvent):
    """
    An event that represents when a file becomes visible
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileHiddenEvent(ContentPassiveEvent):
    """
    An event that represents when a file becomes hidden
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileCreateEvent(ContentPassiveEvent):
    """
    An event that represents when a file is created
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileDeleteRemove(ContentPassiveEvent):
    """
    An event that represents when a file is deleted
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileSaveEvent(ContentPassiveEvent):
    """
    An event that represents saving a file
    """

    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class FileScrollEvent(ContentPassiveEvent):
    def __init__(self, eventTime: datetime, scrollPosition: int):
        super().__init__(eventTime)
        self.scrollPosition = scrollPosition

    def get_scroll_position(self) -> int:
        return self.scrollPosition


class ContentActiveEvent(ContentEvent, ABC):
    """
    An event that represents active content editing
    """


class FileEditEvent(ContentActiveEvent):
    def __init__(self, eventTime: datetime):
        super().__init__(eventTime)


class ClipboardPasteEvent(ContentActiveEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class ClipboardCopyEvent(ContentActiveEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content


class CellAddEvent(ContentActiveEvent):
    def __init__(self, eventTime: datetime, cellId: str):
        super().__init__(eventTime)
        self.cellId = cellId

    def get_cell_id(self) -> str:
        return self.cellId


class ClipboardCutEvent(ContentActiveEvent):
    def __init__(self, eventTime: datetime, content: str):
        super().__init__(eventTime)
        self.content = content

    def get_content(self) -> str:
        return self.content
