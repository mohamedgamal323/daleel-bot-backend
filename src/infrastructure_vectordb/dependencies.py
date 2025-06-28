"""Infrastructure VectorDB dependencies - vector database implementations"""

from src.application.vectordb.vector_db import VectorDB
from src.domain.persistence.asset_repository import AssetRepository

from .memory_vector_db import MemoryVectorDB
from .qdrant_vector_db import QdrantVectorDB


def get_vector_db(vector_db_name: str, asset_repo: AssetRepository) -> VectorDB:
    """Get vector database implementation based on configuration"""
    if vector_db_name.lower() == "qdrant":
        return QdrantVectorDB(asset_repo)
    else:
        return MemoryVectorDB(asset_repo)


# Infrastructure vectordb exports
__all__ = [
    "get_vector_db",
]
