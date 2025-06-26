import os
from ...application.interfaces.llm_provider import LLMProvider

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
        if openai is None or self.api_key is None:
            # Fallback for environments without openai package or key
            return f"OpenAI response to: {prompt}"
        self._ensure_client()
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message["content"].strip()

    def embed(self, text: str) -> list[float]:
        if openai is None or self.api_key is None:
            return [float(sum(ord(c) for c in text))]
        self._ensure_client()
        resp = openai.Embedding.create(model=self.embed_model, input=text)
        return resp["data"][0]["embedding"]
