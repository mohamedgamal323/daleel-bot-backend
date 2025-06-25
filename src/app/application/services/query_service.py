from typing import Iterable
from ..interfaces.asset_repository import AssetRepository
from ...domain.entities.asset import Asset


class QueryService:
    def __init__(self, asset_repo: AssetRepository):
        self._asset_repo = asset_repo

    def query(self, domain_id, text: str) -> Iterable[Asset]:
        assets = self._asset_repo.list(domain_id)
        return [a for a in assets if text.lower() in (a.content or a.name).lower()]
