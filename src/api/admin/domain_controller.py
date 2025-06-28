from fastapi import APIRouter, Depends
from src.application.services.domain_service import DomainService

router = APIRouter(prefix="/domains", tags=["admin-domains"])


@router.get("/")
async def list_domains(service: DomainService = Depends()):
    domains = await service.list_domains()
    return [{"id": str(d.id), "name": d.name} for d in domains]
