from fastapi import APIRouter
from src.app.api.v1.domains import service as domain_service

router = APIRouter(prefix="/domains", tags=["admin-domains"])


@router.get("/")
async def list_domains():
    domains = domain_service.list_domains()
    return [{"id": str(d.id), "name": d.name} for d in domains]
