"""Application integration dependencies - external service providers"""

from typing import Optional
from fastapi import Depends
from src.common.config import get_settings
from ..integration.llm_provider import LLMProvider
from ..vectordb.vector_db import VectorDB


def get_llm_provider() -> Optional[LLMProvider]:
    """Get LLM provider implementation based on configuration"""
    settings = get_settings()
    provider_name = getattr(settings, 'LLM_PROVIDER', 'openai')
    
    if provider_name.lower() == "openai":
        from src.infrastructure_integration.openai_llm import OpenAILLM
        return OpenAILLM()
    elif provider_name.lower() == "cohere":
        from src.infrastructure_integration.cohere_llm import CohereLLM
        return CohereLLM()
    return None


def get_vector_db() -> VectorDB:
    """Get vector database implementation based on configuration"""
    from src.domain.persistence.dependencies import get_asset_repository
    
    settings = get_settings()
    vector_db_name = getattr(settings, 'VECTOR_DB', 'memory')
    asset_repo = get_asset_repository()
    
    if vector_db_name.lower() == "qdrant":
        from src.infrastructure_vectordb.qdrant_vector_db import QdrantVectorDB
        return QdrantVectorDB(asset_repo)
    else:
        from src.infrastructure_vectordb.memory_vector_db import MemoryVectorDB
        return MemoryVectorDB(asset_repo)


# Application integration exports
__all__ = [
    "get_llm_provider",
    "get_vector_db",
]
