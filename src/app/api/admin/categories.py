from fastapi import APIRouter
from src.app.api.v1.categories import service as category_service

router = APIRouter(prefix="/categories", tags=["admin-categories"])


@router.get("/{domain_id}")
async def list_categories(domain_id):
    categories = category_service.list_categories(domain_id)
    return [{"id": str(c.id), "name": c.name} for c in categories]
