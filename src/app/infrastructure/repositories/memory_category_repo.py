from typing import Iterable, List
from ...domain.entities.category import Category
from ...application.interfaces.category_repository import CategoryRepository


class MemoryCategoryRepository(CategoryRepository):
    def __init__(self) -> None:
        self.categories: List[Category] = []

    def add(self, category: Category) -> None:
        self.categories.append(category)

    def list(self, domain_id) -> Iterable[Category]:
        return [c for c in self.categories if c.domain_id == domain_id]
