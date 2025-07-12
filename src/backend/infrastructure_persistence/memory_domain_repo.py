from typing import List
from uuid import UUID
from src.backend.domain.entities.domain import Domain
from src.backend.domain.persistence.domain_repository import DomainRepository


class MemoryDomainRepository(DomainRepository):
    def __init__(self) -> None:
        self.domains: List[Domain] = []

    async def add(self, domain: Domain) -> None:
        self.domains.append(domain)

    async def get(self, domain_id: UUID, include_deleted: bool = False) -> Domain | None:
        for d in self.domains:
            if d.id == domain_id:
                if include_deleted or not d.is_deleted():
                    return d
        return None

    async def get_by_name(self, name: str, include_deleted: bool = False) -> Domain | None:
        for d in self.domains:
            if d.name == name:
                if include_deleted or not d.is_deleted():
                    return d
        return None

    async def list(self, include_deleted: bool = False) -> List[Domain]:
        if include_deleted:
            return list(self.domains)
        return [d for d in self.domains if not d.is_deleted()]

    async def update(self, domain: Domain) -> None:
        for i, d in enumerate(self.domains):
            if d.id == domain.id:
                domain.update()
                self.domains[i] = domain
                break

    async def soft_delete(self, domain_id: UUID) -> None:
        domain = await self.get(domain_id, include_deleted=True)
        if domain:
            domain.soft_delete()

    async def restore(self, domain_id: UUID) -> None:
        domain = await self.get(domain_id, include_deleted=True)
        if domain:
            domain.restore()
