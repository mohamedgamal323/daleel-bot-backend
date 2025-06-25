from abc import ABC, abstractmethod
from typing import Iterable
from ...domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def add(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, domain_id) -> Iterable[Category]:
        raise NotImplementedError
