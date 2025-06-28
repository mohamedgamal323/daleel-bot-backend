from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.asset import Asset


class AssetRepository(ABC):
    @abstractmethod
    async def add(self, asset: Asset) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, asset_id: UUID) -> Asset | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, domain_id: UUID) -> List[Asset]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, asset: Asset) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, asset_id: UUID) -> None:
        raise NotImplementedError
