import ast

from content_log.code_versions_log.code_file import CodeFile
from content_log.execution_log.execution_result import ExecutionCompositeResult
from processor.learning_goal.learning_goal import LearningGoal


class EditRunCycle:
    """
    This class represents an execution with all relevants details
    """

    def __init__(
        self,
        execution: ExecutionCompositeResult,
        code: CodeFile,
        previous_runned_code: CodeFile,
        previous_successful_runned_code: CodeFile,
    ):
        self.execution = execution
        self.code = code
        self.previous_runned_code = previous_runned_code
        self.previous_successful_runned_code = previous_successful_runned_code

    def get_execution(self) -> ExecutionCompositeResult:
        return self.execution

    def get_code(self) -> CodeFile:
        return self.code

    def get_applied_ast_items(self) -> list[ast.AST]:
        return self.previous_runned_code.get_added_ast_items(self.code)

    def get_applied_learning_goals(
        self, learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        lines_changed = self.previous_runned_code.get_line_numbers_of_added_code(
            self.code
        )

        return self.code.get_learning_goals_applied_on_lines(
            lines_changed, learning_goals
        )

    def get_learning_goals_in_error(self) -> list[LearningGoal]:
        error = self.execution.get_error()
        if error is not None:
            return [error.get_error_type(self.code)]
        return []

    def get_error_type_method_2(
        self, learning_goals: list[LearningGoal]
    ) -> list[LearningGoal]:
        error = self.execution.get_error()
        if error is None:
            return []

        error_types = []
        for goal in learning_goals:
            if goal.found_in_error(
                error.get_error_name(), error.get_traceback(), self.code.get_code()
            ):
                error_types.append(goal)

        return error_types

    def get_modifications(self) -> str:
        return self.code.get_code_difference(self.previous_runned_code)
