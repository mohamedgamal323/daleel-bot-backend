from typing import List
from uuid import UUID
from src.domain.persistence.category_repository import CategoryRepository
from src.domain.entities.category import Category


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self._repo = repo

    async def create_category(self, name: str, domain_id: UUID) -> Category:
        category = Category(name=name, domain_id=domain_id)
        await self._repo.add(category)
        return category

    async def list_categories(self, domain_id: UUID) -> List[Category]:
        return await self._repo.list(domain_id)
