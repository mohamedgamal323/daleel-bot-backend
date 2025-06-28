from typing import List
from src.domain.persistence.domain_repository import DomainRepository
from src.domain.entities.domain import Domain


class DomainService:
    def __init__(self, repo: DomainRepository):
        self._repo = repo

    async def create_domain(self, name: str) -> Domain:
        domain = Domain(name=name)
        await self._repo.add(domain)
        return domain

    async def list_domains(self) -> List[Domain]:
        return await self._repo.list()
