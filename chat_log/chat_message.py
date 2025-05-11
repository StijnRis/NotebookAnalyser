import re
from abc import ABC
from datetime import datetime

from langdetect import detect

from chat_log.analyser.chat_message_analyser import ChatMessageAnalyser


class ChatMessage(ABC):
    """
    A single chat message
    """

    def __init__(
        self,
        time: datetime,
        body: str,
        chat_message_analyser: ChatMessageAnalyser,
    ):
        self.time = time
        self.body = body
        self.chat_message_analyser = chat_message_analyser

    def get_time(self):
        return self.time

    def get_body(self):
        return self.body

    def get_length(self):
        return len(self.body)

    def get_included_code_snippets(self):
        codes = []
        matches = re.finditer(
            r"(\`\`\`python|\`)((.|\n)+?)\`{1,3}", self.body, re.DOTALL
        )
        for match in matches:
            code_snippet = match.group(2)
            codes.append(code_snippet.strip())
        return codes

    def contains_code(self):
        # Check for function calls or assignments
        if re.search(r"\b(print|input|float|int|str|len)\(", self.body):
            return True

        # Check for variable assignments ('variable = something')
        if re.search(r"\b\w+\s*=\s*[^=\n]+", self.body):
            return True

        # check for if statements
        if re.search(r"\bif\s+.*\s*:\s*", self.body):
            return True

        # Look for other common Python syntax
        if (
            re.search(r"\bdef\s+\w+\s*\(.*\):", self.body)
            or re.search(r"\bclass\s+\w+\s*\(.*\):", self.body)
            or re.search(r"\bimport\s+\w+", self.body)
            or re.search(r"\bfrom\s+\w+\s+import\s+\w+", self.body)
        ):
            return True

        return False

    def get_language(self):
        result = detect(self.body)
        if result == None:
            return "unknown"
        return result
