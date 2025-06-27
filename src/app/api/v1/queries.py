from fastapi import APIRouter, Depends
from uuid import UUID
from src.app.application.services.query_service import QueryService
from src.app.core.config import Settings, get_settings
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository
from src.app.infrastructure.providers import get_llm_provider, get_vector_db

router = APIRouter(prefix="/queries", tags=["queries"])


def get_asset_repo() -> MemoryAssetRepository:
    return MemoryAssetRepository()


def get_service(
    settings: Settings = Depends(get_settings),
    repo: MemoryAssetRepository = Depends(get_asset_repo),
) -> QueryService:
    llm = get_llm_provider(settings.LLM_PROVIDER)
    vector_db = get_vector_db(settings.VECTOR_DB, asset_repo=repo)
    return QueryService(llm=llm, vector_db=vector_db)


@router.get("/")
async def query(
    domain_id: UUID,
    text: str,
    service: QueryService = Depends(get_service),
):
    answer, assets = service.query(domain_id, text)
    return {
        "answer": answer,
        "assets": [{"id": str(a.id), "name": a.name} for a in assets],
    }
