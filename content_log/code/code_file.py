from file_log.code.source_code import SourceCode


class CodeFile(SourceCode):
    def __init__(self, code: str, path: str):
        super().__init__(code)
        self.path = path

    def get_path(self) -> str:
        return self.path
        