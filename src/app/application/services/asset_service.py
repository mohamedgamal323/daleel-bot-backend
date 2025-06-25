from typing import Iterable
from ..interfaces.asset_repository import AssetRepository
from ...domain.entities.asset import Asset
from ...domain.enums.asset_type import AssetType


class AssetService:
    def __init__(self, repo: AssetRepository):
        self._repo = repo

    def create_asset(self, name: str, domain_id, asset_type: AssetType, content: str | None = None, category_id=None) -> Asset:
        asset = Asset(name=name, domain_id=domain_id, asset_type=asset_type, content=content, category_id=category_id)
        self._repo.add(asset)
        return asset

    def list_assets(self, domain_id) -> Iterable[Asset]:
        return self._repo.list(domain_id)
