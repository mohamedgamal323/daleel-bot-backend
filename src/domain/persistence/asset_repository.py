from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.asset import Asset


class AssetRepository(ABC):
    @abstractmethod
    async def add(self, asset: Asset) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, asset_id: UUID, include_deleted: bool = False) -> Asset | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, domain_id: UUID | None = None, category_id: UUID | None = None, include_deleted: bool = False) -> List[Asset]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, asset: Asset) -> None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, asset_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def restore(self, asset_id: UUID) -> None:
        raise NotImplementedError
