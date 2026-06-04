from typing import Literal
import re


class RouterAgent:
    def classify_intent(self, user_input: str) -> Literal["summary", "quiz", "doubt", "search", "exam_prep"]:
        text = user_input.lower()
        if any(keyword in text for keyword in ["summarize", "summary", "revise", "short note", "revision"]):
            return "summary"
        if any(keyword in text for keyword in ["quiz", "mcq", "viva", "question paper", "exam questions"]):
            return "quiz"
        if any(keyword in text for keyword in ["explain", "why", "how", "what is", "define", "solve", "doubt"]):
            return "doubt"
        if any(keyword in text for keyword in ["search", "find", "lookup", "find in notes", "search inside"]):
            return "search"
        if any(keyword in text for keyword in ["exam prep", "prepare", "revision plan", "study plan", "finals"]):
            return "exam_prep"
        if re.search(r"\?", user_input):
            return "doubt"
        return "summary"
