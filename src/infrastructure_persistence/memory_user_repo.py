from typing import List
from uuid import UUID
from src.domain.entities.user import User
from src.domain.persistence.user_repository import UserRepository


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: List[User] = []

    async def add(self, user: User) -> None:
        self.users.append(user)

    async def get(self, user_id: UUID, include_deleted: bool = False) -> User | None:
        for u in self.users:
            if u.id == user_id:
                if include_deleted or not u.is_deleted():
                    return u
        return None

    async def get_by_username(self, username: str, include_deleted: bool = False) -> User | None:
        for u in self.users:
            if u.username == username:
                if include_deleted or not u.is_deleted():
                    return u
        return None

    async def list(self, include_deleted: bool = False) -> List[User]:
        if include_deleted:
            return list(self.users)
        return [u for u in self.users if not u.is_deleted()]

    async def update(self, user: User) -> None:
        for i, u in enumerate(self.users):
            if u.id == user.id:
                user.update()
                self.users[i] = user
                break

    async def soft_delete(self, user_id: UUID) -> None:
        user = await self.get(user_id, include_deleted=True)
        if user:
            user.soft_delete()

    async def restore(self, user_id: UUID) -> None:
        user = await self.get(user_id, include_deleted=True)
        if user:
            user.restore()
