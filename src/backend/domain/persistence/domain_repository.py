from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.domain import Domain


class DomainRepository(ABC):
    @abstractmethod
    async def add(self, domain: Domain) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, domain_id: UUID, include_deleted: bool = False) -> Domain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str, include_deleted: bool = False) -> Domain | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, include_deleted: bool = False) -> List[Domain]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, domain: Domain) -> None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, domain_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def restore(self, domain_id: UUID) -> None:
        raise NotImplementedError
