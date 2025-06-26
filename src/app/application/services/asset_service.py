from typing import Iterable
from ..interfaces.asset_repository import AssetRepository
from ..interfaces.llm_provider import LLMProvider
from ..interfaces.vector_db import VectorDB
from ...domain.entities.asset import Asset
from ...domain.enums.asset_type import AssetType


class AssetService:
    def __init__(self, repo: AssetRepository, llm: LLMProvider | None = None, vector_db: VectorDB | None = None):
        self._repo = repo
        self._llm = llm
        self._vector_db = vector_db

    def create_asset(self, name: str, domain_id, asset_type: AssetType, content: str | None = None, category_id=None) -> Asset:
        asset = Asset(name=name, domain_id=domain_id, asset_type=asset_type, content=content, category_id=category_id)
        self._repo.add(asset)
        if self._llm and self._vector_db and content:
            embedding = self._llm.embed(content)
            self._vector_db.add(domain_id, asset.id, embedding)
        return asset

    def list_assets(self, domain_id) -> Iterable[Asset]:
        return self._repo.list(domain_id)
