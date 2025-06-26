from fastapi import APIRouter, Depends
from uuid import UUID
from src.app.application.services.asset_service import AssetService
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository
from src.app.domain.enums.asset_type import AssetType
from src.app.core.config import Settings, get_settings
from src.app.infrastructure.providers import get_llm_provider, get_vector_db

router = APIRouter(prefix="/assets", tags=["assets"])


def get_repo() -> MemoryAssetRepository:
    return MemoryAssetRepository()


def get_service(
    settings: Settings = Depends(get_settings),
    repo: MemoryAssetRepository = Depends(get_repo),
) -> AssetService:
    llm = get_llm_provider(settings.LLM_PROVIDER)
    vector_db = get_vector_db(settings.VECTOR_DB, asset_repo=repo)
    return AssetService(repo, llm=llm, vector_db=vector_db)


@router.post("/")
async def create_asset(
    name: str,
    domain_id: UUID,
    asset_type: AssetType,
    content: str | None = None,
    service: AssetService = Depends(get_service),
):
    asset = service.create_asset(
        name=name, domain_id=domain_id, asset_type=asset_type, content=content
    )
    return {"id": str(asset.id), "name": asset.name, "domain_id": str(asset.domain_id)}


@router.get("/{domain_id}")
async def list_assets(
    domain_id: UUID, service: AssetService = Depends(get_service)
):
    assets = service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
