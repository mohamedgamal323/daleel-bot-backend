from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.backend.application.services.category_service import CategoryService
from src.backend.application.dtos.category_dtos import (
    CreateCategoryRequestDto, 
    UpdateCategoryRequestDto, 
    CategoryResponseDto
)

router = APIRouter(prefix="/categories", tags=["categories"])


def category_to_response_dto(category) -> CategoryResponseDto:
    """Convert category entity to response DTO"""
    return CategoryResponseDto(
        id=category.id,
        name=category.name,
        domain_id=category.domain_id,
        created_at=category.created_at,
        updated_at=category.updated_at,
        deleted_at=category.deleted_at
    )


def category_response_dto_to_dict(dto: CategoryResponseDto) -> dict:
    """Convert CategoryResponseDto to API response dict"""
    return {
        "id": str(dto.id),
        "name": dto.name,
        "domain_id": str(dto.domain_id),
        "created_at": dto.created_at.isoformat() if dto.created_at else None,
        "updated_at": dto.updated_at.isoformat() if dto.updated_at else None,
        "deleted_at": dto.deleted_at.isoformat() if dto.deleted_at else None,
    }


@router.post("/")
async def create_category(
    request: CreateCategoryRequestDto,
    service: CategoryService = Depends(),
):
    category = await service.create_category(request)
    dto = category_to_response_dto(category)
    return category_response_dto_to_dict(dto)


@router.get("/")
async def list_all_categories(
    include_deleted: bool = Query(False, description="Include soft-deleted categories"),
    service: CategoryService = Depends()
):
    categories = await service.list_all_categories(include_deleted=include_deleted)
    dtos = [category_to_response_dto(c) for c in categories]
    return [category_response_dto_to_dict(dto) for dto in dtos]


@router.get("/domain/{domain_id}")
async def list_categories_by_domain(
    domain_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted categories"),
    service: CategoryService = Depends()
):
    categories = await service.list_categories(domain_id, include_deleted=include_deleted)
    dtos = [category_to_response_dto(c) for c in categories]
    return [category_response_dto_to_dict(dto) for dto in dtos]


@router.get("/{category_id}")
async def get_category(
    category_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted category"),
    service: CategoryService = Depends()
):
    category = await service.get_category(category_id, include_deleted=include_deleted)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    dto = category_to_response_dto(category)
    return category_response_dto_to_dict(dto)


@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    request: UpdateCategoryRequestDto,
    service: CategoryService = Depends(),
):
    category = await service.update_category(category_id, request)
    dto = category_to_response_dto(category)
    return category_response_dto_to_dict(dto)


@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(),
):
    await service.delete_category(category_id)
    return {"message": "Category deleted successfully"}


@router.post("/{category_id}/restore")
async def restore_category(
    category_id: UUID,
    service: CategoryService = Depends(),
):
    category = await service.restore_category(category_id)
    dto = category_to_response_dto(category)
    return category_response_dto_to_dict(dto)
