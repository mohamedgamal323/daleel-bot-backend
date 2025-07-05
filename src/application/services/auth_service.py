from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone
from uuid import UUID
from typing import Optional

from src.domain.entities.user import User
from src.application.dtos.auth_dtos import (
    LoginCredentials, LoginResponse, TokenRefreshRequest, 
    ChangePasswordRequest, ResetPasswordRequest, TokenPayload
)
from src.domain.enums.role import Role
from src.domain.persistence.user_repository import UserRepository
from src.domain.persistence.dependencies import get_user_repository
from src.application.security.jwt_manager import JWTManager, PasswordSecurity


class AuthService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self._user_repo = user_repo

    async def login(self, credentials: LoginCredentials) -> LoginResponse:
        """Authenticate user and return tokens"""
        # Get user by username
        user = await self._user_repo.get_by_username(credentials.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is inactive"
            )
        
        # Verify password
        if not PasswordSecurity.verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        await self._user_repo.update(user)
        
        # Create tokens
        access_token = JWTManager.create_access_token(user.id, user.username, user.role)
        refresh_token = JWTManager.create_refresh_token(user.id, user.username, user.role)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user={
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "is_active": user.is_active
            }
        )

    async def refresh_token(self, request: TokenRefreshRequest) -> LoginResponse:
        """Refresh access token using refresh token"""
        token_payload = JWTManager.decode_token(request.refresh_token)
        
        if not token_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        if token_payload.token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        if JWTManager.is_token_expired(token_payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user to ensure they still exist and are active
        user = await self._user_repo.get(token_payload.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token = JWTManager.create_access_token(user.id, user.username, user.role)
        new_refresh_token = JWTManager.create_refresh_token(user.id, user.username, user.role)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user={
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "is_active": user.is_active
            }
        )

    async def change_password(self, user_id: UUID, request: ChangePasswordRequest) -> bool:
        """Change user password"""
        user = await self._user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not PasswordSecurity.verify_password(request.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password and update
        user.password_hash = PasswordSecurity.hash_password(request.new_password)
        user.updated_at = datetime.now(timezone.utc)
        await self._user_repo.update(user)
        
        return True

    async def reset_password_admin(self, user_id: UUID, request: ResetPasswordRequest) -> bool:
        """Reset user password (admin only)"""
        user = await self._user_repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Hash new password and update
        user.password_hash = PasswordSecurity.hash_password(request.new_password)
        user.updated_at = datetime.now(timezone.utc)
        await self._user_repo.update(user)
        
        return True

    async def get_current_user_from_token(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        token_payload = JWTManager.decode_token(token)
        
        if not token_payload:
            return None
        
        if token_payload.token_type != "access":
            return None
        
        if JWTManager.is_token_expired(token_payload):
            return None
        
        user = await self._user_repo.get(token_payload.user_id)
        if not user or not user.is_active:
            return None
        
        return user
