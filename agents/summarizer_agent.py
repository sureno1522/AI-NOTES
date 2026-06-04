from models.llm_client import LLMService
from utils.prompt_helpers import SUMMARY_PROMPT


class SummarizerAgent:
    def __init__(self):
        self.llm = LLMService()

    def summarize(self, context: str) -> str:
        prompt = SUMMARY_PROMPT.format(context=context)
        return self.llm.respond(prompt, max_tokens=420)
