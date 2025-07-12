from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Set
from uuid import UUID

from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.enums.permission import Permission, get_role_permissions
from src.application.services.auth_service import AuthService


# HTTP Bearer token security
security = HTTPBearer()


async def get_auth_service() -> AuthService:
    """Get the auth service dependency"""
    from src.domain.persistence.dependencies import get_user_repository
    return AuthService(get_user_repository())


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Get the current authenticated user from JWT token"""
    token = credentials.credentials
    user = await auth_service.get_current_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get the current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(required_role: Role):
    """Dependency to require a specific role"""
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}"
            )
        return current_user
    return role_checker


def require_permission(required_permission: Permission):
    """Dependency to require a specific permission"""
    async def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        user_permissions = get_role_permissions(current_user.role)
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required permission: {required_permission.value}"
            )
        return current_user
    return permission_checker


def require_permissions(required_permissions: Set[Permission]):
    """Dependency to require multiple permissions"""
    async def permissions_checker(current_user: User = Depends(get_current_active_user)) -> User:
        user_permissions = get_role_permissions(current_user.role)
        if not required_permissions.issubset(user_permissions):
            missing_permissions = required_permissions - user_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Missing: {[p.value for p in missing_permissions]}"
            )
        return current_user
    return permissions_checker


# Common role dependencies
require_global_admin = require_role(Role.GLOBAL_ADMIN)
require_domain_admin = require_role(Role.DOMAIN_ADMIN)
require_user = require_role(Role.USER)

# Common permission dependencies  
require_user_read = require_permission(Permission.READ_USER)
require_user_write = require_permission(Permission.CREATE_USER)
require_user_delete = require_permission(Permission.DELETE_USER)

require_domain_read = require_permission(Permission.READ_DOMAIN)
require_domain_write = require_permission(Permission.CREATE_DOMAIN)
require_domain_delete = require_permission(Permission.DELETE_DOMAIN)

require_category_read = require_permission(Permission.READ_CATEGORY)
require_category_write = require_permission(Permission.CREATE_CATEGORY)
require_category_delete = require_permission(Permission.DELETE_CATEGORY)

require_asset_read = require_permission(Permission.READ_ASSET)
require_asset_write = require_permission(Permission.CREATE_ASSET)
require_asset_delete = require_permission(Permission.DELETE_ASSET)
