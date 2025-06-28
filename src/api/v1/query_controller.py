from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.query_service import QueryService
from src.common.dependencies import get_asset_service

router = APIRouter(prefix="/queries", tags=["queries"])


def get_service() -> QueryService:
    # For now, we'll create a simple service
    # In the future, this should be properly integrated with the asset service
    asset_service = get_asset_service()
    return QueryService(asset_service)
    return QueryService(llm=llm, vector_db=vector_db)


@router.get("/")
async def query(
    domain_id: UUID,
    text: str,
    service: QueryService = Depends(get_service),
):
    answer, assets = service.query(domain_id, text)
    return {
        "answer": answer,
        "assets": [{"id": str(a.id), "name": a.name} for a in assets],
    }
