from fastapi import APIRouter
from uuid import UUID
from src.app.application.services.asset_service import AssetService
from src.app.infrastructure.repositories.memory_asset_repo import MemoryAssetRepository
from src.app.domain.enums.asset_type import AssetType

router = APIRouter(prefix="/assets", tags=["assets"])

repo = MemoryAssetRepository()
service = AssetService(repo)


@router.post("/")
async def create_asset(name: str, domain_id: UUID, asset_type: AssetType, content: str | None = None):
    asset = service.create_asset(name=name, domain_id=domain_id, asset_type=asset_type, content=content)
    return {"id": str(asset.id), "name": asset.name, "domain_id": str(asset.domain_id)}


@router.get("/{domain_id}")
async def list_assets(domain_id: UUID):
    assets = service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
