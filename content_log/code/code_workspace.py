from file_log.code.code_file import CodeFile
from file_log.code.source_code import SourceCode


class CodeWorkspace:
    def __init__(self, source_codes: list[SourceCode]):
        self.source_codes = source_codes
    
    def get_code_notebook(self, path: str) -> SourceCode:
        for source_code in self.source_codes:
            if isinstance(source_code, CodeFile) and source_code.get_path() == path:
                return source_code
        
        raise ValueError(f"Code notebook with path {path} not found")