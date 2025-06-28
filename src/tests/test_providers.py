from uuid import uuid4
from src.common.dependencies import (
    get_llm_provider,
    get_vector_db,
)
from src.infrastructure_integration.cohere_llm import CohereLLM
from src.infrastructure_integration.openai_llm import OpenAILLM
from src.infrastructure_vectordb.qdrant_vector_db import QdrantVectorDB
from src.infrastructure_vectordb.memory_vector_db import MemoryVectorDB
from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository
from src.application.services.query_service import QueryService
from src.domain.entities.asset import Asset
from src.domain.enums.asset_type import AssetType


def test_get_llm_provider():
    assert isinstance(get_llm_provider("cohere"), CohereLLM)
    assert isinstance(get_llm_provider("openai"), OpenAILLM)


def test_get_vector_db():
    repo = MemoryAssetRepository()
    assert isinstance(get_vector_db("memory", asset_repo=repo), MemoryVectorDB)
    assert isinstance(get_vector_db("qdrant"), QdrantVectorDB)


def test_query_service_with_memory_db_and_llm():
    repo = MemoryAssetRepository()
    domain_id = uuid4()
    asset = Asset(name="doc", domain_id=domain_id, asset_type=AssetType.DOCUMENT, content="hello")
    repo.add(asset)
    vector_db = MemoryVectorDB(repo)
    llm = OpenAILLM()
    vector_db.add(domain_id, asset.id, llm.embed(asset.content))
    service = QueryService(llm=llm, vector_db=vector_db)
    answer, assets = service.query(domain_id, "hello")
    assert answer.startswith("OpenAI response")
    assert len(list(assets)) == 1
