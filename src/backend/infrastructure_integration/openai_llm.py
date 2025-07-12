import os
from src.backend.application.integration.llm_provider import LLMProvider

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    openai = None


class OpenAILLM(LLMProvider):
    """LLM provider that delegates to OpenAI's API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "gpt-3.5-turbo",
        embed_model: str = "text-embedding-ada-002",
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_API_BASE")
        self.model = model
        self.embed_model = embed_model

    def _ensure_client(self) -> None:
        if openai is None:
            raise RuntimeError("openai package is not installed")
        openai.api_key = self.api_key
        if self.base_url:
            openai.base_url = self.base_url

    def complete(self, prompt: str) -> str:
        """Generate a completion for the given prompt."""
        self._ensure_client()
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}") from e

    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for the given text."""
        self._ensure_client()
        try:
            response = openai.Embedding.create(
                model=self.embed_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"OpenAI embedding error: {e}") from e
