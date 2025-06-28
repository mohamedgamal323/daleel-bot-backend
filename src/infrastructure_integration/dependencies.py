"""Infrastructure integration dependencies - external service providers"""

from typing import Optional
from src.application.integration.llm_provider import LLMProvider
from src.application.vectordb.vector_db import VectorDB
from src.domain.persistence.asset_repository import AssetRepository
from src.common.config import get_settings

from .cohere_llm import CohereLLM
from .openai_llm import OpenAILLM

# Import from the new vectordb infrastructure
from src.infrastructure_vectordb.dependencies import get_vector_db as _get_vector_db


def get_llm_provider(provider_name: str = "openai") -> Optional[LLMProvider]:
    """Get LLM provider implementation based on configuration"""
    if provider_name.lower() == "openai":
        return OpenAILLM()
    elif provider_name.lower() == "cohere":
        return CohereLLM()
    return None


def get_vector_db(vector_db_name: str, asset_repo: AssetRepository) -> VectorDB:
    """Get vector database implementation based on configuration"""
    return _get_vector_db(vector_db_name, asset_repo)


# Infrastructure integration exports
__all__ = [
    "get_llm_provider",
    "get_vector_db",
]
