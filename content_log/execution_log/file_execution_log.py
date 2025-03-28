from datetime import datetime
from typing import List, Tuple

from content_log.execution_log.execution_result import (
    ExecutionErrorResult,
    ExecutionResult,
)


class FileExecutionLog:
    def __init__(self, executions: list[ExecutionResult]):
        self.executions = executions

        self.executions.sort(key=lambda x: x.get_time())

    def get_execution_outputs(self) -> list[ExecutionResult]:
        return self.executions

    def get_runtime_errors(self) -> list[ExecutionErrorResult]:
        runtime_errors = []
        for entry in self.executions:
            if isinstance(entry, ExecutionErrorResult):
                runtime_errors.append(entry)
        return runtime_errors

    def get_start_time(self) -> datetime:
        if len(self.executions) == 0:
            return datetime.fromtimestamp(0)
        return self.executions[0].get_time()

    def get_end_time(self) -> datetime:
        if len(self.executions) == 0:
            return datetime.fromtimestamp(0)
        return self.executions[-1].get_time()

    def get_amount_of_executions(self):
        return len(self.executions)

    def get_amount_of_runtime_errors(self):
        total = 0
        for entry in self.executions:
            if isinstance(entry, ExecutionErrorResult):
                total += 1

        return total

    def get_execution_sequence(self) -> List[Tuple[datetime, bool]]:
        """
        Returns a list of tuples with the event time and execution result (success or failure).
        """
        results = []
        for entry in self.executions:
            success = not isinstance(entry, ExecutionErrorResult)
            results.append((entry.get_time(), success))
        return results

    def get_event_sequence(self) -> List[Tuple[datetime, str]]:
        """
        Returns a list of tuples with the event time and the event type.
        """
        results = []
        for entry in self.executions:
            results.append((entry.get_time(), entry.__class__.__name__))

        return results
