from fastapi import APIRouter, Depends
from uuid import UUID
from src.application.services.query_service import QueryService
from src.application.dtos.query_dtos import (
    QueryRequestDto,
    QueryResponseDto,
    AssetSummaryDto
)

router = APIRouter(prefix="/queries", tags=["queries"])


@router.get("/")
async def query(
    domain_id: UUID,
    text: str,
    service: QueryService = Depends(),
):
    # Create request DTO
    request_dto = QueryRequestDto(domain_id=domain_id, text=text)
    
    # Call service with DTO
    answer, assets = service.query(request_dto)
    
    # Create response DTO
    asset_summaries = [AssetSummaryDto(id=a.id, name=a.name) for a in assets]
    response_dto = QueryResponseDto(answer=answer, assets=asset_summaries)
    
    # Convert to dict for API response
    return {
        "answer": response_dto.answer,
        "assets": [{"id": str(asset.id), "name": asset.name} for asset in response_dto.assets],
    }
