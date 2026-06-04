import requests
from typing import Optional
from utils.config import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    OLLAMA_API_KEY,
    GEMINI_HOST,
    GEMINI_MODEL,
    GEMINI_API_KEY,
)


class OllamaClient:
    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL, temperature: float = 0.2):
        self.host = host.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.headers = {"Content-Type": "application/json"}
        if OLLAMA_API_KEY:
            self.headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

    def generate(self, prompt: str, max_tokens: int = 512, stop: Optional[list[str]] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "stop": stop or [],
        }
        url = f"{self.host}/v1/completions"
        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                return self._generate_chat(prompt=prompt, max_tokens=max_tokens, stop=stop)
            raise

        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0].get("text", "").strip()
        return result.get("text", "").strip()

    def _generate_chat(self, prompt: str, max_tokens: int = 512, stop: Optional[list[str]] = None) -> str:
        url = f"{self.host}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": self.temperature,
        }
        if stop:
            payload["stop"] = stop

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {})
            return message.get("content", "").strip()
        return result.get("text", "").strip()


class GeminiClient:
    def __init__(self, host: str = GEMINI_HOST, model: str = GEMINI_MODEL, temperature: float = 0.2):
        self.host = host.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.api_key = GEMINI_API_KEY
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def generate(self, prompt: str, max_tokens: int = 512, stop: Optional[list[str]] = None) -> str:
        url = f"{self.host}/v1/models/{self.model}:generate"
        payload = {
            "input": prompt,
            "temperature": self.temperature,
            "maxOutputTokens": max_tokens,
        }
        if stop:
            payload["stop"] = stop

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0].get("content", "").strip()
        output = result.get("output")
        if isinstance(output, dict):
            return output.get("text", "").strip()
        if isinstance(output, list) and len(output) > 0:
            first = output[0]
            if isinstance(first, dict):
                return first.get("content", "").strip()
        return result.get("text", "").strip()


class LLMService:
    def __init__(self):
        self.gemini_client = GeminiClient() if GEMINI_API_KEY else None
        self.ollama_client = OllamaClient() if OLLAMA_HOST else None
        if self.gemini_client is None and self.ollama_client is None:
            raise RuntimeError(
                "No LLM backend configured. Set GEMINI_API_KEY or OLLAMA_HOST in your .env file."
            )

    def respond(self, prompt: str, context: str = "", max_tokens: int = 512) -> str:
        if context:
            prompt = f"Context:\n{context}\n\nInstructions:\n{prompt}"

        last_error = None
        if self.gemini_client is not None:
            try:
                return self.gemini_client.generate(prompt=prompt, max_tokens=max_tokens)
            except requests.exceptions.HTTPError as exc:
                last_error = exc
                if exc.response is not None and exc.response.status_code == 404:
                    # Gemini not available for this model / endpoint; try Ollama if configured.
                    pass
                else:
                    # Keep trying Ollama if configured after any Gemini HTTP issue.
                    pass
            except Exception as exc:
                last_error = exc

        if self.ollama_client is not None:
            try:
                return self.ollama_client.generate(prompt=prompt, max_tokens=max_tokens)
            except Exception as exc:
                last_error = exc

        raise RuntimeError(
            "LLM generation failed. Check your Gemini or Ollama configuration. "
            f"Last error: {last_error}"
        )
