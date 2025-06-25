from abc import ABC, abstractmethod
from typing import Iterable
from ...domain.entities.domain import Domain


class DomainRepository(ABC):
    @abstractmethod
    def add(self, domain: Domain) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Iterable[Domain]:
        raise NotImplementedError
