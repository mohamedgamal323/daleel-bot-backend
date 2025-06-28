from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["admin-categories"])


@router.get("/{domain_id}")
async def list_categories(domain_id: UUID, service: CategoryService = Depends()):
    categories = await service.list_categories(domain_id)
    return [{"id": str(c.id), "name": c.name} for c in categories]
