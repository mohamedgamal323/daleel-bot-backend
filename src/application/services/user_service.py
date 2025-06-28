from typing import List
from uuid import UUID
from fastapi import Depends
from src.domain.persistence.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.persistence.dependencies import get_user_repository


class UserService:
    def __init__(self, repo: UserRepository = Depends(get_user_repository)):
        self._repo = repo

    async def create_user(self, username: str, role: Role) -> User:
        user = User(username=username, role=role)
        await self._repo.add(user)
        return user

    async def get_user(self, user_id: UUID) -> User | None:
        return await self._repo.get(user_id)

    async def list_users(self) -> List[User]:
        return await self._repo.list()
