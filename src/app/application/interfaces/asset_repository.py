from abc import ABC, abstractmethod
from typing import Iterable
from ...domain.entities.asset import Asset


class AssetRepository(ABC):
    @abstractmethod
    def add(self, asset: Asset) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, domain_id) -> Iterable[Asset]:
        raise NotImplementedError
