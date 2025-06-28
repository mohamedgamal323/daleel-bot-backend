from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[User]:
        raise NotImplementedError
