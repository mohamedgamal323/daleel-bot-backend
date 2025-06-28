from typing import List
from uuid import UUID
from src.domain.entities.asset import Asset
from src.domain.persistence.asset_repository import AssetRepository


class MemoryAssetRepository(AssetRepository):
    def __init__(self) -> None:
        self.assets: List[Asset] = []

    async def add(self, asset: Asset) -> None:
        self.assets.append(asset)

    async def get(self, asset_id: UUID) -> Asset | None:
        for a in self.assets:
            if a.id == asset_id:
                return a
        return None

    async def list(self, domain_id: UUID) -> List[Asset]:
        return [a for a in self.assets if a.domain_id == domain_id]

    async def update(self, asset: Asset) -> None:
        for i, a in enumerate(self.assets):
            if a.id == asset.id:
                self.assets[i] = asset
                break

    async def delete(self, asset_id: UUID) -> None:
        self.assets = [a for a in self.assets if a.id != asset_id]
