from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/")
async def create_category(
    name: str,
    domain_id: UUID,
    service: CategoryService = Depends(),
):
    category = await service.create_category(name=name, domain_id=domain_id)
    return {"id": str(category.id), "name": category.name}


@router.get("/{domain_id}")
async def list_categories(
    domain_id: UUID, service: CategoryService = Depends()
):
    categories = await service.list_categories(domain_id)
    return [{"id": str(c.id), "name": c.name} for c in categories]
