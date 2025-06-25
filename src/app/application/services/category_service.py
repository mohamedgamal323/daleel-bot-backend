from typing import Iterable
from ..interfaces.category_repository import CategoryRepository
from ...domain.entities.category import Category


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self._repo = repo

    def create_category(self, name: str, domain_id) -> Category:
        category = Category(name=name, domain_id=domain_id)
        self._repo.add(category)
        return category

    def list_categories(self, domain_id) -> Iterable[Category]:
        return self._repo.list(domain_id)
