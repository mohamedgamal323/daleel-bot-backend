from typing import List
from uuid import UUID
from fastapi import Depends
from src.domain.persistence.asset_repository import AssetRepository
from ..integration.llm_provider import LLMProvider
from ..vectordb.vector_db import VectorDB
from src.domain.entities.asset import Asset
from src.domain.enums.asset_type import AssetType
from src.domain.persistence.dependencies import get_asset_repository
from ..integration.dependencies import get_llm_provider, get_vector_db


class AssetService:
    def __init__(
        self, 
        repo: AssetRepository = Depends(get_asset_repository),
        llm: LLMProvider | None = Depends(get_llm_provider),
        vector_db: VectorDB | None = Depends(get_vector_db)
    ):
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
