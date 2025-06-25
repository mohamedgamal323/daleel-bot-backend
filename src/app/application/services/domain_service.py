from typing import Iterable
from ..interfaces.domain_repository import DomainRepository
from ...domain.entities.domain import Domain


class DomainService:
    def __init__(self, repo: DomainRepository):
        self._repo = repo

    def create_domain(self, name: str) -> Domain:
        domain = Domain(name=name)
        self._repo.add(domain)
        return domain

    def list_domains(self) -> Iterable[Domain]:
        return self._repo.list()
