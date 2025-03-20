class ExecutionResult:
    def __init__(self, result: dict):
        self.result = result
        self.check_invariants()