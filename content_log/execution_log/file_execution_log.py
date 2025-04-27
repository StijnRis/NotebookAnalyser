from datetime import datetime
from functools import lru_cache
from typing import List, Tuple

from content_log.execution_log.execution_result import (
    ExecutionErrorResult,
    ExecutionResult,
    ExecutionSuccessResult,
)
from content_log.progression.progression_with_datetime import ProgressionWithDatetime


class FileExecutionLog:
    def __init__(self, executions: list[ExecutionResult]):
        self.executions = executions

        self.executions.sort(key=lambda x: x.get_time())
    
    def check_invariants(self):
        # Check that the log entries are sorted by time
        for i in range(1, len(self.executions)):
            assert (
                self.executions[i].get_time() >= self.executions[i - 1].get_time()
            ), "Log entries should be sorted by event time"

    def get_executions(self) -> list[ExecutionResult]:
        return self.executions
    
    def get_events(self) -> list[ExecutionResult]:
        return self.executions

    def get_runtime_errors(self) -> list[ExecutionErrorResult]:
        runtime_errors = []
        for entry in self.executions:
            if isinstance(entry, ExecutionErrorResult):
                runtime_errors.append(entry)
        return runtime_errors
    
    def get_first_successful_execution_after(self, time: datetime) -> ExecutionResult | None:
        for entry in self.executions:
            if entry.get_time() > time and isinstance(entry, ExecutionSuccessResult):
                return entry
        return None

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
    
    @lru_cache(maxsize=None)
    def get_output_progression(self):
        execution_outputs = self.get_executions()

        times: list[datetime] = []
        output_progression: list[float] = []

        # Check if user has executed any code
        if len(execution_outputs) == 0:
            return ProgressionWithDatetime(times, output_progression)

        last_execution_output = execution_outputs[-1]

        for execution_output in execution_outputs:
            output_similarity = execution_output.get_output_similarity_ratio(
                last_execution_output
            )

            times.append(execution_output.get_time())
            output_progression.append(output_similarity)

        return ProgressionWithDatetime(times, output_progression)
