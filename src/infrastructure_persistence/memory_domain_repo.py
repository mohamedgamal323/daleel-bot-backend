from typing import List
from uuid import UUID
from src.domain.entities.domain import Domain
from src.domain.persistence.domain_repository import DomainRepository


class MemoryDomainRepository(DomainRepository):
    def __init__(self) -> None:
        self.domains: List[Domain] = []

    async def add(self, domain: Domain) -> None:
        self.domains.append(domain)

    async def get(self, domain_id: UUID) -> Domain | None:
        for d in self.domains:
            if d.id == domain_id:
                return d
        return None

    async def get_by_name(self, name: str) -> Domain | None:
        for d in self.domains:
            if d.name == name:
                return d
        return None

    async def list(self) -> List[Domain]:
        return list(self.domains)

    async def update(self, domain: Domain) -> None:
        for i, d in enumerate(self.domains):
            if d.id == domain.id:
                self.domains[i] = domain
                break

    async def delete(self, domain_id: UUID) -> None:
        self.domains = [d for d in self.domains if d.id != domain_id]
