from content_log.code.code_version_manager import CodeVersionManager
from content_log.editing_log.editing_notebook_log import EditingNotebookLog
from content_log.file_log import FileLog
from execution_log.execution_log import ExecutionLog


class NotebookLog(FileLog):
    """
    
    """
    
    def __init__(self, editing_notebook_log: EditingNotebookLog, code_version_manager: CodeVersionManager):
        super().__init__(editing_notebook_log, code_version_manager)