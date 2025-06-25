from abc import ABC, abstractmethod
from typing import Iterable
from ...domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Iterable[User]:
        raise NotImplementedError
