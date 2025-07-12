from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.backend.application.services.asset_service import AssetService
from src.backend.domain.enums.asset_type import AssetType
from pydantic import BaseModel

router = APIRouter(prefix="/assets", tags=["admin-assets"])


class CreateAssetRequest(BaseModel):
    name: str
    domain_id: UUID
    asset_type: AssetType
    content: str | None = None
    category_id: UUID | None = None


class UpdateAssetRequest(BaseModel):
    name: str | None = None
    content: str | None = None
    category_id: UUID | None = None


def asset_response(asset):
    return {
        "id": str(asset.id),
        "name": asset.name,
        "domain_id": str(asset.domain_id),
        "asset_type": asset.asset_type.value,
        "content": asset.content,
        "category_id": str(asset.category_id) if asset.category_id else None,
        "created_at": asset.created_at.isoformat() if asset.created_at else None,
        "updated_at": asset.updated_at.isoformat() if asset.updated_at else None,
        "deleted_at": asset.deleted_at.isoformat() if asset.deleted_at else None,
        "is_deleted": asset.is_deleted(),
    }


@router.post("/")
async def create_asset(
    request: CreateAssetRequest,
    service: AssetService = Depends(),
):
    asset = await service.create_asset(
        name=request.name,
        domain_id=request.domain_id,
        asset_type=request.asset_type,
        content=request.content,
        category_id=request.category_id
    )
    return asset_response(asset)


@router.get("/")
async def list_all_assets(
    domain_id: UUID | None = Query(None, description="Filter by domain ID"),
    category_id: UUID | None = Query(None, description="Filter by category ID"),
    include_deleted: bool = Query(True, description="Include soft-deleted assets (admin default: true)"),
    service: AssetService = Depends()
):
    assets = await service.list_assets(domain_id=domain_id, category_id=category_id, include_deleted=include_deleted)
    return [asset_response(a) for a in assets]


@router.get("/{asset_id}")
async def get_asset(
    asset_id: UUID,
    include_deleted: bool = Query(True, description="Include soft-deleted asset (admin default: true)"),
    service: AssetService = Depends()
):
    asset = await service.get_asset(asset_id, include_deleted=include_deleted)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_response(asset)


@router.put("/{asset_id}")
async def update_asset(
    asset_id: UUID,
    request: UpdateAssetRequest,
    service: AssetService = Depends(),
):
    asset = await service.update_asset(asset_id, name=request.name, content=request.content, category_id=request.category_id)
    return asset_response(asset)


@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: UUID,
    service: AssetService = Depends(),
):
    await service.delete_asset(asset_id)
    return {"message": "Asset deleted successfully"}


@router.post("/{asset_id}/restore")
async def restore_asset(
    asset_id: UUID,
    service: AssetService = Depends(),
):
    asset = await service.restore_asset(asset_id)
    return asset_response(asset)
