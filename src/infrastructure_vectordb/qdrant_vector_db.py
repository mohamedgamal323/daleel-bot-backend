from typing import Iterable
from uuid import UUID
import os

from src.domain.entities.asset import Asset
from src.application.vectordb.vector_db import VectorDB
from src.domain.persistence.asset_repository import AssetRepository

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
except Exception:  # pragma: no cover - optional dependency
    QdrantClient = None
    qmodels = None


class QdrantVectorDB(VectorDB):
    """Vector DB backed by Qdrant."""

    def __init__(
        self,
        url: str = "http://localhost:6333",
        api_key: str | None = None,
        collection: str = "assets",
        asset_repo: AssetRepository | None = None,
    ) -> None:
        self.asset_repo = asset_repo
        self.collection = collection
        if QdrantClient is not None:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = None

    def add(self, domain_id: UUID, asset_id: UUID, embedding: list[float]) -> None:
        """Store embedding for an asset within a domain."""
        if self.client is None:
            raise RuntimeError("Qdrant client is not available")
        
        try:
            # Ensure collection exists
            self._ensure_collection(len(embedding))
            
            # Add point to collection
            self.client.upsert(
                collection_name=self.collection,
                points=[
                    qmodels.PointStruct(
                        id=str(asset_id),
                        vector=embedding,
                        payload={
                            "domain_id": str(domain_id),
                            "asset_id": str(asset_id)
                        }
                    )
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Qdrant add error: {e}") from e

    async def search(self, domain_id: UUID, embedding: list[float], top_k: int = 5) -> Iterable[Asset]:
        """Search for relevant assets by embedding within a domain."""
        if self.client is None:
            raise RuntimeError("Qdrant client is not available")
        
        if self.asset_repo is None:
            raise RuntimeError("Asset repository is required for search")
        
        try:
            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection,
                query_vector=embedding,
                query_filter=qmodels.Filter(
                    must=[
                        qmodels.FieldCondition(
                            key="domain_id",
                            match=qmodels.MatchValue(value=str(domain_id))
                        )
                    ]
                ),
                limit=top_k
            )
            
            # Get asset IDs from search results
            asset_ids = [UUID(hit.payload["asset_id"]) for hit in search_result]
            
            # Fetch actual assets from repository
            assets = []
            for asset_id in asset_ids:
                asset = await self.asset_repo.get(asset_id)
                if asset:
                    assets.append(asset)
            
            return assets
        except Exception as e:
            raise RuntimeError(f"Qdrant search error: {e}") from e

    def _ensure_collection(self, vector_size: int) -> None:
        """Ensure the collection exists with the right vector configuration."""
        if self.client is None:
            return
        
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=qmodels.VectorParams(
                        size=vector_size,
                        distance=qmodels.Distance.COSINE
                    )
                )
        except Exception as e:
            raise RuntimeError(f"Qdrant collection setup error: {e}") from e
