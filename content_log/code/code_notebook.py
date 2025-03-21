from file_log.code.code_file import CodeFile


class CodeNotebook(CodeFile):
    def __init__(self, code: str, path: str):
        super().__init__(code, path)
    