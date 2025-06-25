from fastapi import APIRouter
from src.app.api.v1.assets import service as asset_service

router = APIRouter(prefix="/assets", tags=["admin-assets"])


@router.get("/{domain_id}")
async def list_assets(domain_id):
    assets = asset_service.list_assets(domain_id)
    return [{"id": str(a.id), "name": a.name} for a in assets]
