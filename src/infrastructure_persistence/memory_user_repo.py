from typing import List
from uuid import UUID
from src.domain.entities.user import User
from src.domain.persistence.user_repository import UserRepository


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: List[User] = []

    async def add(self, user: User) -> None:
        self.users.append(user)

    async def get(self, user_id: UUID) -> User | None:
        for u in self.users:
            if u.id == user_id:
                return u
        return None

    async def list(self) -> List[User]:
        return list(self.users)
