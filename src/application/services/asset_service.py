from typing import List
from uuid import UUID
from src.domain.persistence.asset_repository import AssetRepository
from ..integration.llm_provider import LLMProvider
from ..vectordb.vector_db import VectorDB
from src.domain.entities.asset import Asset
from src.domain.enums.asset_type import AssetType


class AssetService:
    def __init__(self, repo: AssetRepository, llm: LLMProvider | None = None, vector_db: VectorDB | None = None):
        self._repo = repo
        self._llm = llm
        self._vector_db = vector_db

    async def create_asset(self, name: str, domain_id: UUID, asset_type: AssetType, content: str | None = None, category_id: UUID | None = None) -> Asset:
        asset = Asset(name=name, domain_id=domain_id, asset_type=asset_type, content=content, category_id=category_id)
        await self._repo.add(asset)
        if self._llm and self._vector_db and content:
            embedding = self._llm.embed(content)
            self._vector_db.add(domain_id, asset.id, embedding)
        return asset

    async def list_assets(self, domain_id: UUID) -> List[Asset]:
        return await self._repo.list(domain_id)
