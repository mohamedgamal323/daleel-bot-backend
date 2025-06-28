from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.asset_service import AssetService
from src.common.dependencies import get_asset_service
from src.domain.enums.asset_type import AssetType

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/")
async def create_asset(
    name: str,
    domain_id: UUID,
    asset_type: AssetType,
    content: str | None = None,
    service: AssetService = Depends(get_asset_service),
):
    asset = await service.create_asset(
        name=name, domain_id=domain_id, asset_type=asset_type, content=content
    )
    return {"id": str(asset.id), "name": asset.name, "domain_id": str(asset.domain_id)}


@router.get("/{domain_id}")
async def list_assets(
    domain_id: UUID, service: AssetService = Depends(get_asset_service)
):
    assets = await service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
