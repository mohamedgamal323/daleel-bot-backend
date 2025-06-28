from typing import List
from uuid import UUID
from src.domain.entities.category import Category
from src.domain.persistence.category_repository import CategoryRepository


class MemoryCategoryRepository(CategoryRepository):
    def __init__(self) -> None:
        self.categories: List[Category] = []

    async def add(self, category: Category) -> None:
        self.categories.append(category)

    async def get(self, category_id: UUID) -> Category | None:
        for c in self.categories:
            if c.id == category_id:
                return c
        return None

    async def get_by_name(self, name: str, domain_id: UUID) -> Category | None:
        for c in self.categories:
            if c.name == name and c.domain_id == domain_id:
                return c
        return None

    async def list(self, domain_id: UUID) -> List[Category]:
        return [c for c in self.categories if c.domain_id == domain_id]

    async def list_all(self) -> List[Category]:
        return list(self.categories)

    async def update(self, category: Category) -> None:
        for i, c in enumerate(self.categories):
            if c.id == category.id:
                self.categories[i] = category
                break

    async def delete(self, category_id: UUID) -> None:
        self.categories = [c for c in self.categories if c.id != category_id]
