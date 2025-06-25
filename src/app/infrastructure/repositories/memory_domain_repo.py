from typing import Iterable, List
from ...domain.entities.domain import Domain
from ...application.interfaces.domain_repository import DomainRepository


class MemoryDomainRepository(DomainRepository):
    def __init__(self) -> None:
        self.domains: List[Domain] = []

    def add(self, domain: Domain) -> None:
        self.domains.append(domain)

    def list(self) -> Iterable[Domain]:
        return list(self.domains)
