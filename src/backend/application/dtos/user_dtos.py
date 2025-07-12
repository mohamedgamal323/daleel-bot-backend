from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime
from src.backend.domain.enums.role import Role


@dataclass
class CreateUserRequestDto:
    """DTO for creating a new user"""
    username: str
    role: Role


@dataclass
class UserRegistrationDto:
    """DTO for user registration with password hash"""
    username: str
    email: str
    password_hash: str
    role: Role


@dataclass
class UpdateUserRequestDto:
    """DTO for updating an existing user"""
    username: Optional[str] = None
    role: Optional[Role] = None


@dataclass
class UserResponseDto:
    """DTO for user response"""
    id: UUID
    username: str
    role: Role
    email: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
