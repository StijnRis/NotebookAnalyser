# from datetime import datetime

# from content_log.code.code_file import CodeFile
# from content_log.code.source_code import SourceCode


# class CodeWorkspace:
#     def __init__(self, time: datetime, code_files: list[CodeFile]):
#         self.time = time
#         self.code_files = code_files

#         self.check_invariants()

#     def check_invariants(self):
#         for source_code in self.code_files:
#             assert source_code.get_time() == self.get_time()

#         # for source_code in self.source_codes:
#         #     source_code.check_invariants()

#     def get_time(self) -> datetime:
#         return self.time

#     def get_code_file(self, path: str) -> SourceCode:
#         for source_code in self.code_files:
#             if isinstance(source_code, CodeFile) and source_code.get_path() == path:
#                 return source_code

#         raise ValueError(f"Code file with path {path} not found")

#     def get_all_code_as_string(self):
#         """
#         Get all the code of the notebook as a string.
#         """
#         return "\n\n".join([source_code.get_code() for source_code in self.code_files])

#     def get_ast_difference_ratio(self, other_workspace: "CodeWorkspace"):
#         """
#         Calculate the difference in AST between this workspace and another workspace.

#         Each file is weighted equally.
#         """

#         total_files = len(self.code_files)
#         total_difference = 0

#         for source_code in self.code_files:
#             other_source_code = other_workspace.get_code_file(source_code.get_path())

#             total_difference += source_code.get_ast_difference_ratio(other_source_code)

#         return total_difference / total_files
