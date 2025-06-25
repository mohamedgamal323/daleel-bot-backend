from fastapi import APIRouter
from src.app.application.services.domain_service import DomainService
from src.app.infrastructure.repositories.memory_domain_repo import MemoryDomainRepository

router = APIRouter(prefix="/domains", tags=["domains"])

repo = MemoryDomainRepository()
service = DomainService(repo)


@router.post("/")
async def create_domain(name: str):
    domain = service.create_domain(name)
    return {"id": str(domain.id), "name": domain.name}


@router.get("/")
async def list_domains():
    domains = service.list_domains()
    return [{"id": str(d.id), "name": d.name} for d in domains]
