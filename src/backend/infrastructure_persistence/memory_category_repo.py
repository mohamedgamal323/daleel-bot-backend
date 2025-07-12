from typing import List
from uuid import UUID
from src.backend.domain.entities.category import Category
from src.backend.domain.persistence.category_repository import CategoryRepository


class MemoryCategoryRepository(CategoryRepository):
    def __init__(self) -> None:
        self.categories: List[Category] = []

    async def add(self, category: Category) -> None:
        self.categories.append(category)

    async def get(self, category_id: UUID, include_deleted: bool = False) -> Category | None:
        for c in self.categories:
            if c.id == category_id:
                if include_deleted or not c.is_deleted():
                    return c
        return None

    async def get_by_name(self, name: str, domain_id: UUID, include_deleted: bool = False) -> Category | None:
        for c in self.categories:
            if c.name == name and c.domain_id == domain_id:
                if include_deleted or not c.is_deleted():
                    return c
        return None

    async def list(self, domain_id: UUID, include_deleted: bool = False) -> List[Category]:
        categories = [c for c in self.categories if c.domain_id == domain_id]
        if include_deleted:
            return categories
        return [c for c in categories if not c.is_deleted()]

    async def list_all(self, include_deleted: bool = False) -> List[Category]:
        if include_deleted:
            return list(self.categories)
        return [c for c in self.categories if not c.is_deleted()]

    async def update(self, category: Category) -> None:
        for i, c in enumerate(self.categories):
            if c.id == category.id:
                category.update()
                self.categories[i] = category
                break

    async def soft_delete(self, category_id: UUID) -> None:
        category = await self.get(category_id, include_deleted=True)
        if category:
            category.soft_delete()

    async def restore(self, category_id: UUID) -> None:
        category = await self.get(category_id, include_deleted=True)
        if category:
            category.restore()
