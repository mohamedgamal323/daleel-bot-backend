from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.backend.application.services.domain_service import DomainService
from src.backend.application.dtos.domain_dtos import (
    CreateDomainRequestDto,
    UpdateDomainRequestDto,
    DomainResponseDto
)

router = APIRouter(prefix="/domains", tags=["domains"])


def domain_to_response_dto(domain) -> DomainResponseDto:
    """Convert domain entity to response DTO"""
    return DomainResponseDto(
        id=domain.id,
        name=domain.name,
        created_at=domain.created_at,
        updated_at=domain.updated_at,
        deleted_at=domain.deleted_at
    )


def domain_response_dto_to_dict(dto: DomainResponseDto) -> dict:
    """Convert DomainResponseDto to API response dict"""
    return {
        "id": str(dto.id),
        "name": dto.name,
        "created_at": dto.created_at.isoformat() if dto.created_at else None,
        "updated_at": dto.updated_at.isoformat() if dto.updated_at else None,
        "deleted_at": dto.deleted_at.isoformat() if dto.deleted_at else None,
    }


@router.post("/")
async def create_domain(
    request: CreateDomainRequestDto,
    service: DomainService = Depends()
):
    domain = await service.create_domain(request)
    dto = domain_to_response_dto(domain)
    return domain_response_dto_to_dict(dto)


@router.get("/")
async def list_domains(
    include_deleted: bool = Query(False, description="Include soft-deleted domains"),
    service: DomainService = Depends()
):
    domains = await service.list_domains(include_deleted=include_deleted)
    dtos = [domain_to_response_dto(d) for d in domains]
    return [domain_response_dto_to_dict(dto) for dto in dtos]


@router.get("/{domain_id}")
async def get_domain(
    domain_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted domain"),
    service: DomainService = Depends()
):
    domain = await service.get_domain(domain_id, include_deleted=include_deleted)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    dto = domain_to_response_dto(domain)
    return domain_response_dto_to_dict(dto)


@router.put("/{domain_id}")
async def update_domain(
    domain_id: UUID,
    request: UpdateDomainRequestDto,
    service: DomainService = Depends(),
):
    domain = await service.update_domain(domain_id, request)
    dto = domain_to_response_dto(domain)
    return domain_response_dto_to_dict(dto)


@router.delete("/{domain_id}")
async def delete_domain(
    domain_id: UUID,
    service: DomainService = Depends(),
):
    await service.delete_domain(domain_id)
    return {"message": "Domain deleted successfully"}


@router.post("/{domain_id}/restore")
async def restore_domain(
    domain_id: UUID,
    service: DomainService = Depends(),
):
    domain = await service.restore_domain(domain_id)
    dto = domain_to_response_dto(domain)
    return domain_response_dto_to_dict(dto)
