from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.backend.application.services.category_service import CategoryService
from pydantic import BaseModel

router = APIRouter(prefix="/categories", tags=["admin-categories"])


class CreateCategoryRequest(BaseModel):
    name: str
    domain_id: UUID


class UpdateCategoryRequest(BaseModel):
    name: str | None = None
    domain_id: UUID | None = None


def category_response(category):
    return {
        "id": str(category.id),
        "name": category.name,
        "domain_id": str(category.domain_id),
        "created_at": category.created_at.isoformat() if category.created_at else None,
        "updated_at": category.updated_at.isoformat() if category.updated_at else None,
        "deleted_at": category.deleted_at.isoformat() if category.deleted_at else None,
        "is_deleted": category.is_deleted(),
    }


@router.post("/")
async def create_category(
    request: CreateCategoryRequest,
    service: CategoryService = Depends(),
):
    category = await service.create_category(name=request.name, domain_id=request.domain_id)
    return category_response(category)


@router.get("/")
async def list_all_categories(
    include_deleted: bool = Query(True, description="Include soft-deleted categories (admin default: true)"),
    service: CategoryService = Depends()
):
    categories = await service.list_all_categories(include_deleted=include_deleted)
    return [category_response(c) for c in categories]


@router.get("/domain/{domain_id}")
async def list_categories_by_domain(
    domain_id: UUID,
    include_deleted: bool = Query(True, description="Include soft-deleted categories (admin default: true)"),
    service: CategoryService = Depends()
):
    categories = await service.list_categories(domain_id, include_deleted=include_deleted)
    return [category_response(c) for c in categories]


@router.get("/{category_id}")
async def get_category(
    category_id: UUID,
    include_deleted: bool = Query(True, description="Include soft-deleted category (admin default: true)"),
    service: CategoryService = Depends()
):
    category = await service.get_category(category_id, include_deleted=include_deleted)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_response(category)


@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    request: UpdateCategoryRequest,
    service: CategoryService = Depends(),
):
    category = await service.update_category(category_id, name=request.name, domain_id=request.domain_id)
    return category_response(category)


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
    return category_response(category)
