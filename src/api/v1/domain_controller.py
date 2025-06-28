from fastapi import APIRouter, Depends
from src.application.services.domain_service import DomainService

router = APIRouter(prefix="/domains", tags=["domains"])


@router.post("/")
async def create_domain(
    name: str, service: DomainService = Depends()
):
    domain = await service.create_domain(name)
    return {"id": str(domain.id), "name": domain.name}


@router.get("/")
async def list_domains(service: DomainService = Depends()):
    domains = await service.list_domains()
    return [{"id": str(d.id), "name": d.name} for d in domains]
