from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID
from ...domain.entities.asset import Asset


class VectorDB(ABC):
    @abstractmethod
    def add(self, domain_id: UUID, asset_id: UUID, embedding: list[float]) -> None:
        """Store embedding for an asset within a domain."""
        pass

    @abstractmethod
    def search(self, domain_id: UUID, embedding: list[float], top_k: int = 5) -> Iterable[Asset]:
        """Search for relevant assets by embedding within a domain."""
        pass
