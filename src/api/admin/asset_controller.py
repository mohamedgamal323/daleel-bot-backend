from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.asset_service import AssetService
from src.common.dependencies import get_asset_service

router = APIRouter(prefix="/assets", tags=["admin-assets"])


@router.get("/{domain_id}")
async def list_assets(domain_id: UUID, service: AssetService = Depends(get_asset_service)):
    assets = await service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
