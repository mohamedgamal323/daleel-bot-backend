from typing import Iterable
from uuid import UUID
import os

from ...domain.entities.asset import Asset
from ...application.interfaces.vector_db import VectorDB
from ..repositories.memory_asset_repo import MemoryAssetRepository

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
        asset_repo: MemoryAssetRepository | None = None,
    ) -> None:
        self.asset_repo = asset_repo
        self.collection = collection
        if QdrantClient is not None:
            self.client = QdrantClient(url=url, api_key=api_key)
            try:
                self.client.get_collection(collection)
            except Exception:
                if qmodels is not None:
                    self.client.recreate_collection(
                        collection_name=collection,
                        vectors_config=qmodels.VectorParams(
                            size=1536,
                            distance=qmodels.Distance.COSINE,
                        ),
                    )
        else:
            self.client = None

    def add(self, domain_id: UUID, asset_id: UUID, embedding: list[float]) -> None:
        if self.client is None:
            return
        if qmodels is None:
            return
        point = qmodels.PointStruct(
            id=str(asset_id),
            vector=embedding,
            payload={"domain_id": str(domain_id)},
        )
        self.client.upsert(collection_name=self.collection, points=[point])

    def search(
        self, domain_id: UUID, embedding: list[float], top_k: int = 5
    ) -> Iterable[Asset]:
        if self.client is None or qmodels is None or self.asset_repo is None:
            return []
        result = self.client.search(
            collection_name=self.collection,
            query_vector=embedding,
            limit=top_k,
            query_filter=qmodels.Filter(
                must=[
                    qmodels.FieldCondition(
                        key="domain_id",
                        match=qmodels.MatchValue(value=str(domain_id)),
                    )
                ]
            ),
        )
        asset_ids = {UUID(point.id) for point in result}
        return [a for a in self.asset_repo.list(domain_id) if a.id in asset_ids]
