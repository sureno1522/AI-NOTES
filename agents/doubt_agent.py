from models.llm_client import LLMService
from utils.prompt_helpers import DOUBT_PROMPT


class DoubtAgent:
    def __init__(self):
        self.llm = LLMService()

    def answer_doubt(self, query: str, context: str) -> str:
        prompt = DOUBT_PROMPT.format(query=query, context=context)
        return self.llm.respond(prompt, max_tokens=520)
