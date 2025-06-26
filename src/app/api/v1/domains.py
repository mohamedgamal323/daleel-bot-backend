from fastapi import APIRouter, Depends
from src.app.application.services.domain_service import DomainService
from src.app.infrastructure.repositories.memory_domain_repo import MemoryDomainRepository

router = APIRouter(prefix="/domains", tags=["domains"])


def get_repo() -> MemoryDomainRepository:
    return MemoryDomainRepository()


def get_service(repo: MemoryDomainRepository = Depends(get_repo)) -> DomainService:
    return DomainService(repo)


@router.post("/")
async def create_domain(
    name: str, service: DomainService = Depends(get_service)
):
    domain = service.create_domain(name)
    return {"id": str(domain.id), "name": domain.name}


@router.get("/")
async def list_domains(service: DomainService = Depends(get_service)):
    domains = service.list_domains()
    return [{"id": str(d.id), "name": d.name} for d in domains]
