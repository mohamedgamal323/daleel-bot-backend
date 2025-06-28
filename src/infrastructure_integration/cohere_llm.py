from src.application.integration.llm_provider import LLMProvider


class CohereLLM(LLMProvider):
    def complete(self, prompt: str) -> str:
        return f"Cohere response to: {prompt}"

    def embed(self, text: str) -> list[float]:
        return [float(len(text))]
