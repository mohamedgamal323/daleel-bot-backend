from uuid import uuid4
from src.app.application.services.asset_service import AssetService
from src.app.domain.enums.asset_type import AssetType
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository


def test_create_and_list_asset():
    repo = MemoryAssetRepository()
    service = AssetService(repo)
    domain_id = uuid4()
    service.create_asset("file1", domain_id, AssetType.DOCUMENT, content="hello")
    assets = list(service.list_assets(domain_id))
    assert len(assets) == 1
    assert assets[0].name == "file1"
