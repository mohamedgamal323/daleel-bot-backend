from typing import Iterable, List
from ...domain.entities.asset import Asset
from ...application.interfaces.asset_repository import AssetRepository


class MemoryAssetRepository(AssetRepository):
    def __init__(self) -> None:
        self.assets: List[Asset] = []

    def add(self, asset: Asset) -> None:
        self.assets.append(asset)

    def list(self, domain_id) -> Iterable[Asset]:
        return [a for a in self.assets if a.domain_id == domain_id]
