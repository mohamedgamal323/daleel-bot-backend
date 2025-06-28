from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def add(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, category_id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str, domain_id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, domain_id: UUID) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, category_id: UUID) -> None:
        raise NotImplementedError
