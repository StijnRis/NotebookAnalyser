from content_log.code.code_version_manager import CodeVersionManager
from content_log.editing_log.editing_log import EditingLog


class ContentLog:
    def __init__(self, editing_log: EditingLog, code_version_manager: CodeVersionManager):
        self.editing_log = editing_log
        self.code_version_manager = code_version_manager
    
    def get_editing_log(self) -> EditingLog:
        return self.editing_log

    def get_code_version_manager(self) -> CodeVersionManager:
        return self.code_version_manager