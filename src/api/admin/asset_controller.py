from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.asset_service import AssetService

router = APIRouter(prefix="/assets", tags=["admin-assets"])


@router.get("/{domain_id}")
async def list_assets(domain_id: UUID, service: AssetService = Depends()):
    assets = await service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
