from typing import List


class MemoryAgent:
    def __init__(self):
        self.history: List[dict] = []

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[dict]:
        return self.history[-20:]

    def clear_memory(self) -> None:
        self.history = []
