from typing import Iterable
from uuid import UUID
from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository
from src.domain.entities.asset import Asset
from src.application.vectordb.vector_db import VectorDB


class MemoryVectorDB(VectorDB):
    """A very small in-memory vector DB for tests."""

    def __init__(self, asset_repo: MemoryAssetRepository):
        self._asset_repo = asset_repo
        self._index: dict[UUID, list[tuple[list[float], UUID]]] = {}

    def add(self, domain_id: UUID, asset_id: UUID, embedding: list[float]) -> None:
        self._index.setdefault(domain_id, []).append((embedding, asset_id))

    async def search(self, domain_id: UUID, embedding: list[float], top_k: int = 5) -> Iterable[Asset]:
        scored: list[tuple[float, UUID]] = []
        for emb, asset_id in self._index.get(domain_id, []):
            score = sum(e1 * e2 for e1, e2 in zip(emb, embedding))
            scored.append((score, asset_id))
        scored.sort(reverse=True)
        asset_ids = {a_id for _, a_id in scored[:top_k]}
        assets = await self._asset_repo.list(domain_id)
        return [a for a in assets if a.id in asset_ids]
