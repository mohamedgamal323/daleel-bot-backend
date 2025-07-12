from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.backend.application.services.asset_service import AssetService
from src.backend.application.dtos.asset_dtos import (
    CreateAssetRequestDto,
    UpdateAssetRequestDto,
    AssetResponseDto
)

router = APIRouter(prefix="/assets", tags=["assets"])


def asset_to_response_dto(asset) -> AssetResponseDto:
    """Convert asset entity to response DTO"""
    return AssetResponseDto(
        id=asset.id,
        name=asset.name,
        domain_id=asset.domain_id,
        asset_type=asset.asset_type,
        content=asset.content,
        category_id=asset.category_id,
        created_at=asset.created_at,
        updated_at=asset.updated_at,
        deleted_at=asset.deleted_at
    )


def asset_response_dto_to_dict(dto: AssetResponseDto) -> dict:
    """Convert AssetResponseDto to API response dict"""
    return {
        "id": str(dto.id),
        "name": dto.name,
        "domain_id": str(dto.domain_id),
        "asset_type": dto.asset_type.value,
        "content": dto.content,
        "category_id": str(dto.category_id) if dto.category_id else None,
        "created_at": dto.created_at.isoformat() if dto.created_at else None,
        "updated_at": dto.updated_at.isoformat() if dto.updated_at else None,
        "deleted_at": dto.deleted_at.isoformat() if dto.deleted_at else None,
    }


@router.post("/")
async def create_asset(
    request: CreateAssetRequestDto,
    service: AssetService = Depends(),
):
    asset = await service.create_asset(request)
    dto = asset_to_response_dto(asset)
    return asset_response_dto_to_dict(dto)


@router.get("/")
async def list_assets(
    domain_id: UUID | None = Query(None, description="Filter by domain ID"),
    category_id: UUID | None = Query(None, description="Filter by category ID"),
    include_deleted: bool = Query(False, description="Include soft-deleted assets"),
    service: AssetService = Depends()
):
    assets = await service.list_assets(domain_id=domain_id, category_id=category_id, include_deleted=include_deleted)
    dtos = [asset_to_response_dto(a) for a in assets]
    return [asset_response_dto_to_dict(dto) for dto in dtos]


@router.get("/{asset_id}")
async def get_asset(
    asset_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted asset"),
    service: AssetService = Depends()
):
    asset = await service.get_asset(asset_id, include_deleted=include_deleted)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    dto = asset_to_response_dto(asset)
    return asset_response_dto_to_dict(dto)


@router.put("/{asset_id}")
async def update_asset(
    asset_id: UUID,
    request: UpdateAssetRequestDto,
    service: AssetService = Depends(),
):
    asset = await service.update_asset(asset_id, request)
    dto = asset_to_response_dto(asset)
    return asset_response_dto_to_dict(dto)


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
    dto = asset_to_response_dto(asset)
    return asset_response_dto_to_dict(dto)
