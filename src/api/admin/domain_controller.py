from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.application.services.domain_service import DomainService
from pydantic import BaseModel

router = APIRouter(prefix="/domains", tags=["admin-domains"])


class CreateDomainRequest(BaseModel):
    name: str


class UpdateDomainRequest(BaseModel):
    name: str | None = None


def domain_response(domain):
    return {
        "id": str(domain.id),
        "name": domain.name,
        "created_at": domain.created_at.isoformat() if domain.created_at else None,
        "updated_at": domain.updated_at.isoformat() if domain.updated_at else None,
        "deleted_at": domain.deleted_at.isoformat() if domain.deleted_at else None,
        "is_deleted": domain.is_deleted(),
    }


@router.post("/")
async def create_domain(
    request: CreateDomainRequest,
    service: DomainService = Depends()
):
    domain = await service.create_domain(request.name)
    return domain_response(domain)


@router.get("/")
async def list_domains(
    include_deleted: bool = Query(True, description="Include soft-deleted domains (admin default: true)"),
    service: DomainService = Depends()
):
    domains = await service.list_domains(include_deleted=include_deleted)
    return [domain_response(d) for d in domains]


@router.get("/{domain_id}")
async def get_domain(
    domain_id: UUID,
    include_deleted: bool = Query(True, description="Include soft-deleted domain (admin default: true)"),
    service: DomainService = Depends()
):
    domain = await service.get_domain(domain_id, include_deleted=include_deleted)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain_response(domain)


@router.put("/{domain_id}")
async def update_domain(
    domain_id: UUID,
    request: UpdateDomainRequest,
    service: DomainService = Depends(),
):
    domain = await service.update_domain(domain_id, name=request.name)
    return domain_response(domain)


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
    return domain_response(domain)
