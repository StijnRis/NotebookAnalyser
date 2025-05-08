

from datetime import datetime
from content_log.code_versions_log.source_code import SourceCode


class CodeFile(SourceCode):
    def __init__(self, time: datetime, code: str, path: str):
        super().__init__(time, code)
        self.path = path

    def get_path(self) -> str:
        return self.path
    