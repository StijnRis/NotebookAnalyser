from ast import AST

from processor.learning_goal.learning_goal import LearningGoal


class TypoLearningGoal(LearningGoal):
    def __init__(self):
        super().__init__(
            name="Typo",
            description="This learning goal is applied when a typo is detected in the code.",
        )

    def is_applied_in(self, code: AST) -> bool:
        return False

    def found_in_error(self, error_name: str, traceback: str, code: str) -> bool:
        """
        Detects typo errors using error name and message.
        """
        error_name_l = error_name.lower()
        if "syntaxerror" in error_name_l and "eol" in error_name_l:
            return True
        if "syntaxerror" in error_name_l and (
            "unexpected eof" in error_name_l
            or "unterminated string literal" in error_name_l
        ):
            return True
        # fallback
        return False
