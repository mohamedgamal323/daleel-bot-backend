from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Generate a completion for the given prompt."""
        pass

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for the given text."""
        pass
