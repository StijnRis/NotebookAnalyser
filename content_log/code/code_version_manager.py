from content_log.code.source_code import SourceCode


class CodeVersionManager:
    def __init__(self, codes: list[SourceCode]):
        self.codes = codes