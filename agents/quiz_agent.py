from models.llm_client import LLMService
from utils.prompt_helpers import QUIZ_PROMPT


class QuizAgent:
    def __init__(self):
        self.llm = LLMService()

    def generate_quiz(self, context: str) -> str:
        prompt = QUIZ_PROMPT.format(context=context)
        return self.llm.respond(prompt, max_tokens=520)
