from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.query_service import QueryService

router = APIRouter(prefix="/queries", tags=["queries"])


@router.get("/")
async def query(
    domain_id: UUID,
    text: str,
    service: QueryService = Depends(),
):
    answer, assets = service.query(domain_id, text)
    return {
        "answer": answer,
        "assets": [{"id": str(a.id), "name": a.name} for a in assets],
    }
