from uuid import uuid4
from src.app.infrastructure.providers import (
    get_llm_provider,
    get_vector_db,
    CohereLLM,
    OpenAILLM,
    QdrantVectorDB,
    MemoryVectorDB,
)
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository
from src.app.application.services.query_service import QueryService
from src.app.domain.entities.asset import Asset
from src.app.domain.enums.asset_type import AssetType


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
