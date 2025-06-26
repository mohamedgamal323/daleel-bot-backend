from fastapi import APIRouter, Depends
from uuid import UUID
from src.app.application.services.category_service import CategoryService
from src.app.infrastructure.repositories.memory_category_repo import MemoryCategoryRepository

router = APIRouter(prefix="/categories", tags=["categories"])


def get_repo() -> MemoryCategoryRepository:
    return MemoryCategoryRepository()


def get_service(
    repo: MemoryCategoryRepository = Depends(get_repo),
) -> CategoryService:
    return CategoryService(repo)


@router.post("/")
async def create_category(
    name: str,
    domain_id: UUID,
    service: CategoryService = Depends(get_service),
):
    category = service.create_category(name=name, domain_id=domain_id)
    return {"id": str(category.id), "name": category.name}


@router.get("/{domain_id}")
async def list_categories(
    domain_id: UUID, service: CategoryService = Depends(get_service)
):
    categories = service.list_categories(domain_id)
    return [{"id": str(c.id), "name": c.name} for c in categories]
