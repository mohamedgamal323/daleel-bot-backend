import pytest
from uuid import uuid4
from src.application.services.asset_service import AssetService
from src.domain.enums.asset_type import AssetType
from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository
from src.common.dependencies import get_llm_provider, get_vector_db


@pytest.mark.asyncio
async def test_create_and_list_asset():
    repo = MemoryAssetRepository()
    service = AssetService(repo)
    domain_id = uuid4()
    await service.create_asset("file1", domain_id, AssetType.DOCUMENT, content="hello")
    assets = await service.list_assets(domain_id)
    assert len(assets) == 1
    assert assets[0].name == "file1"


@pytest.mark.asyncio
async def test_asset_service_stores_embedding():
    repo = MemoryAssetRepository()
    llm = get_llm_provider("openai")
    vector_db = get_vector_db("memory", asset_repo=repo)
    service = AssetService(repo, llm=llm, vector_db=vector_db)
    domain_id = uuid4()
    asset = await service.create_asset("doc", domain_id, AssetType.DOCUMENT, content="hello")
    results = vector_db.search(domain_id, llm.embed("hello"))
    assert asset in list(results)
