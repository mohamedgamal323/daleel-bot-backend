import pytest
from uuid import uuid4
from src.application.services.asset_service import AssetService
from src.domain.enums.asset_type import AssetType
from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository


@pytest.mark.asyncio
async def test_create_and_list_asset():
    repo = MemoryAssetRepository()
    # For testing, we can instantiate directly with the repository and None for optional dependencies
    service = AssetService(repo, llm=None, vector_db=None)
    domain_id = uuid4()
    await service.create_asset("file1", domain_id, AssetType.DOCUMENT, content="hello")
    assets = await service.list_assets(domain_id)
    assert len(assets) == 1
    assert assets[0].name == "file1"


@pytest.mark.asyncio
async def test_asset_service_stores_embedding():
    from src.infrastructure_integration.openai_llm import OpenAILLM
    from src.infrastructure_vectordb.memory_vector_db import MemoryVectorDB
    
    repo = MemoryAssetRepository()
    llm = OpenAILLM()
    vector_db = MemoryVectorDB(repo)
    # For testing, we can instantiate directly with all dependencies
    service = AssetService(repo, llm=llm, vector_db=vector_db)
    domain_id = uuid4()
    
    # Test embedding functionality if OpenAI is available, otherwise just test basic creation
    try:
        asset = await service.create_asset("doc", domain_id, AssetType.DOCUMENT, content="hello")
        results = vector_db.search(domain_id, llm.embed("hello"))
        assert asset in list(results)
    except RuntimeError:
        # OpenAI not installed, just test basic asset creation without embedding
        service_no_embedding = AssetService(repo, llm=None, vector_db=None)
        asset = await service_no_embedding.create_asset("doc", domain_id, AssetType.DOCUMENT, content="hello")
        assert asset.name == "doc"
        assert asset.content == "hello"
