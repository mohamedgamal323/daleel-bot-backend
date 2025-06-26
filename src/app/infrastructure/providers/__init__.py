import os

from .openai_llm import OpenAILLM
from .cohere_llm import CohereLLM
from .qdrant_vector_db import QdrantVectorDB
from .memory_vector_db import MemoryVectorDB


def get_llm_provider(name: str):
    """Return an LLM provider instance based on the given name."""
    name = name.lower()
    if name == "cohere":
        return CohereLLM()
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")
    return OpenAILLM(
        api_key=api_key,
        base_url=base_url,
        model=model,
        embed_model=embed_model,
    )


def get_vector_db(name: str, asset_repo=None):
    """Return a vector DB instance based on the given name."""
    name = name.lower()
    if name == "memory":
        return MemoryVectorDB(asset_repo)
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY")
    collection = os.getenv("QDRANT_COLLECTION", "assets")
    return QdrantVectorDB(url=url, api_key=api_key, collection=collection, asset_repo=asset_repo)


__all__ = [
    "OpenAILLM",
    "CohereLLM",
    "QdrantVectorDB",
    "MemoryVectorDB",
    "get_llm_provider",
    "get_vector_db",
]

