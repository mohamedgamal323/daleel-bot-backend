from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from src.domain.persistence.asset_repository import AssetRepository
from ..integration.llm_provider import LLMProvider
from ..vectordb.vector_db import VectorDB
from src.domain.entities.asset import Asset
from src.domain.enums.asset_type import AssetType
from src.domain.persistence.dependencies import get_asset_repository
from ..integration.dependencies import get_llm_provider, get_vector_db
from src.application.dtos.asset_dtos import CreateAssetRequestDto, UpdateAssetRequestDto


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

    async def create_asset(self, dto: CreateAssetRequestDto) -> Asset:
        asset = Asset(
            name=dto.name, 
            domain_id=dto.domain_id, 
            asset_type=dto.asset_type, 
            content=dto.content, 
            category_id=dto.category_id
        )
        await self._repo.add(asset)
        if self._llm and self._vector_db and dto.content:
            embedding = self._llm.embed(dto.content)
            self._vector_db.add(dto.domain_id, asset.id, embedding)
        return asset

    async def get_asset(self, asset_id: UUID, include_deleted: bool = False) -> Asset | None:
        return await self._repo.get(asset_id, include_deleted=include_deleted)

    async def list_assets(self, domain_id: UUID | None = None, category_id: UUID | None = None, include_deleted: bool = False) -> List[Asset]:
        return await self._repo.list(domain_id=domain_id, category_id=category_id, include_deleted=include_deleted)

    async def update_asset(self, asset_id: UUID, dto: UpdateAssetRequestDto) -> Asset:
        asset = await self._repo.get(asset_id, include_deleted=False)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        if dto.name:
            asset.name = dto.name
        
        if dto.content is not None:
            asset.content = dto.content
            # Update vector embedding if content changed
            if self._llm and self._vector_db and dto.content:
                embedding = self._llm.embed(dto.content)
                self._vector_db.update(asset.domain_id, asset.id, embedding)
        
        if dto.category_id is not None:
            asset.category_id = dto.category_id
        
        await self._repo.update(asset)
        return asset

    async def delete_asset(self, asset_id: UUID) -> None:
        asset = await self._repo.get(asset_id, include_deleted=False)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        await self._repo.soft_delete(asset_id)
        
        # Remove from vector database
        if self._vector_db:
            self._vector_db.delete(asset.domain_id, asset.id)

    async def restore_asset(self, asset_id: UUID) -> Asset:
        asset = await self._repo.get(asset_id, include_deleted=True)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        if not asset.is_deleted():
            raise HTTPException(status_code=400, detail="Asset is not deleted")
        
        await self._repo.restore(asset_id)
        
        # Re-add to vector database if content exists
        if self._llm and self._vector_db and asset.content:
            embedding = self._llm.embed(asset.content)
            self._vector_db.add(asset.domain_id, asset.id, embedding)
        
        return await self._repo.get(asset_id, include_deleted=False)
