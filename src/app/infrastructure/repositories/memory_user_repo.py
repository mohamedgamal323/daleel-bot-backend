from typing import Iterable, List
from ...domain.entities.user import User
from ...application.interfaces.user_repository import UserRepository


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: List[User] = []

    def add(self, user: User) -> None:
        self.users.append(user)

    def get(self, user_id) -> User | None:
        for u in self.users:
            if u.id == user_id:
                return u
        return None

    def list(self) -> Iterable[User]:
        return list(self.users)
