from datetime import datetime

from content_log.code.code_file import CodeFile


class CodeVersionsLog:
    def __init__(self, code_file: list[CodeFile]):
        self.code_files = code_file

        self.code_files.sort(key=lambda workspace: workspace.get_time())

        self.check_invariants()

    def check_invariants(self):
        for i in range(len(self.code_files) - 1):
            assert self.code_files[i].get_time() <= self.code_files[i + 1].get_time()

        # for workspace in self.workspaces:
        #     workspace.check_invariants()

    def get_code_files(self) -> list[CodeFile]:
        return self.code_files
    
    def get_amount_of_code_files(self) -> int:
        return len(self.code_files)
    
    def get_start_time(self) -> datetime:
        if len(self.code_files) == 0:
            return datetime.fromtimestamp(0)
        return self.code_files[0].get_time()
    
    def get_end_time(self) -> datetime:
        if len(self.code_files) == 0:
            return datetime.fromtimestamp(0)
        return self.code_files[-1].get_time()

    def get_code_file_at(self, time: datetime) -> CodeFile:
        """
        Get the code content at a certain time.
        """

        for code_file in self.code_files:
            if code_file.get_time() > time:
                return code_file

        print(f"No code file found at time {time}")
        return CodeFile(time, "", "")
