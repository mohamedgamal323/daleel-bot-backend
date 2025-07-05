from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID, include_deleted: bool = False) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str, include_deleted: bool = False) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, include_deleted: bool = False) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def restore(self, user_id: UUID) -> None:
        raise NotImplementedError
