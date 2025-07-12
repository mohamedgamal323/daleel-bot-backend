from typing import List
from uuid import UUID
from src.backend.domain.entities.asset import Asset
from src.backend.domain.persistence.asset_repository import AssetRepository


class MemoryAssetRepository(AssetRepository):
    def __init__(self) -> None:
        self.assets: List[Asset] = []

    async def add(self, asset: Asset) -> None:
        self.assets.append(asset)

    async def get(self, asset_id: UUID, include_deleted: bool = False) -> Asset | None:
        for a in self.assets:
            if a.id == asset_id:
                if include_deleted or not a.is_deleted():
                    return a
        return None

    async def list(self, domain_id: UUID | None = None, category_id: UUID | None = None, include_deleted: bool = False) -> List[Asset]:
        assets = list(self.assets)
        
        # Filter by domain_id if provided
        if domain_id is not None:
            assets = [a for a in assets if a.domain_id == domain_id]
        
        # Filter by category_id if provided
        if category_id is not None:
            assets = [a for a in assets if a.category_id == category_id]
        
        # Filter by deleted status
        if not include_deleted:
            assets = [a for a in assets if not a.is_deleted()]
        
        return assets

    async def update(self, asset: Asset) -> None:
        for i, a in enumerate(self.assets):
            if a.id == asset.id:
                asset.update()
                self.assets[i] = asset
                break

    async def soft_delete(self, asset_id: UUID) -> None:
        asset = await self.get(asset_id, include_deleted=True)
        if asset:
            asset.soft_delete()

    async def restore(self, asset_id: UUID) -> None:
        asset = await self.get(asset_id, include_deleted=True)
        if asset:
            asset.restore()
