from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from src.domain.persistence.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.persistence.dependencies import get_user_repository
from src.application.dtos.user_dtos import CreateUserRequestDto, UpdateUserRequestDto, UserRegistrationDto


class UserService:
    def __init__(self, repo: UserRepository = Depends(get_user_repository)):
        self._repo = repo

    async def create_user(self, dto: CreateUserRequestDto) -> User:
        # Check if user already exists
        existing = await self._repo.get_by_username(dto.username, include_deleted=True)
        if existing and not existing.is_deleted():
            raise HTTPException(status_code=400, detail="User with this username already exists")
        
        user = User(username=dto.username, role=dto.role)
        await self._repo.add(user)
        return user

    async def get_user(self, user_id: UUID, include_deleted: bool = False) -> User | None:
        return await self._repo.get(user_id, include_deleted=include_deleted)

    async def get_user_by_username(self, username: str, include_deleted: bool = False) -> User | None:
        return await self._repo.get_by_username(username, include_deleted=include_deleted)

    async def list_users(self, include_deleted: bool = False) -> List[User]:
        return await self._repo.list(include_deleted=include_deleted)

    async def update_user(self, user_id: UUID, dto: UpdateUserRequestDto) -> User:
        user = await self._repo.get(user_id, include_deleted=False)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if new username conflicts with existing user
        if dto.username and dto.username != user.username:
            existing = await self._repo.get_by_username(dto.username, include_deleted=True)
            if existing and not existing.is_deleted():
                raise HTTPException(status_code=400, detail="User with this username already exists")
            user.username = dto.username
        
        if dto.role:
            user.role = dto.role
        
        await self._repo.update(user)
        return user

    async def delete_user(self, user_id: UUID) -> None:
        user = await self._repo.get(user_id, include_deleted=False)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await self._repo.soft_delete(user_id)

    async def restore_user(self, user_id: UUID) -> User:
        user = await self._repo.get(user_id, include_deleted=True)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user.is_deleted():
            raise HTTPException(status_code=400, detail="User is not deleted")
        
        await self._repo.restore(user_id)
        return await self._repo.get(user_id, include_deleted=False)

    async def register_user(self, dto: UserRegistrationDto) -> User:
        """Register a new user with complete information"""
        # Check if user already exists by username
        existing_username = await self._repo.get_by_username(dto.username, include_deleted=True)
        if existing_username and not existing_username.is_deleted():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Create new user
        user = User(
            username=dto.username,
            email=dto.email,
            password_hash=dto.password_hash,
            role=dto.role,
            is_active=True
        )
        
        await self._repo.add(user)
        return user
