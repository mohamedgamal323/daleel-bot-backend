from fastapi import APIRouter
from uuid import UUID
from src.app.application.services.query_service import QueryService
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository

router = APIRouter(prefix="/queries", tags=["queries"])

asset_repo = MemoryAssetRepository()
service = QueryService(asset_repo)


@router.get("/")
async def query(domain_id: UUID, text: str):
    assets = service.query(domain_id, text)
    return [{"id": str(a.id), "name": a.name} for a in assets]
