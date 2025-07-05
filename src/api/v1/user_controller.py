from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from src.application.services.user_service import UserService
from src.application.services.auth_service import AuthService
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.enums.permission import Permission, get_role_permissions
from src.application.dtos.user_dtos import (
    CreateUserRequestDto,
    UpdateUserRequestDto,
    UserResponseDto
)

router = APIRouter(prefix="/users", tags=["users"])

# HTTP Bearer token security
security = HTTPBearer()


async def extract_current_user_from_token(
    credentials: HTTPAuthorizationCredentials,
    auth_service: AuthService
) -> User:
    """Helper function to extract current user from JWT token"""
    token = credentials.credentials
    user = await auth_service.get_current_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def validate_permission(user: User, required_permission: Permission) -> None:
    """Helper function to validate user permission"""
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    user_permissions = get_role_permissions(user.role.value)
    if required_permission not in user_permissions:
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: {required_permission.value}"
        )


def user_to_response_dto(user: User) -> UserResponseDto:
    """Convert user entity to response DTO"""
    return UserResponseDto(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        deleted_at=user.deleted_at
    )


def user_response_dto_to_dict(dto: UserResponseDto) -> dict:
    """Convert UserResponseDto to API response dict"""
    return {
        "id": str(dto.id),
        "username": dto.username,
        "email": dto.email,
        "role": dto.role.value,
        "is_active": dto.is_active,
        "created_at": dto.created_at.isoformat() if dto.created_at else None,
        "updated_at": dto.updated_at.isoformat() if dto.updated_at else None,
        "deleted_at": dto.deleted_at.isoformat() if dto.deleted_at else None,
    }


@router.post("/")
async def create_user(
    request: CreateUserRequestDto,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends(),
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_permission(current_user, Permission.CREATE_USER)
    
    user = await user_service.create_user(request)
    dto = user_to_response_dto(user)
    return user_response_dto_to_dict(dto)


@router.get("/")
async def list_users(
    include_deleted: bool = Query(False, description="Include soft-deleted users"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends()
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_permission(current_user, Permission.READ_USER)
    
    users = await user_service.list_users(include_deleted=include_deleted)
    dtos = [user_to_response_dto(u) for u in users]
    return [user_response_dto_to_dict(dto) for dto in dtos]


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted user"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends()
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_permission(current_user, Permission.READ_USER)
    
    user = await user_service.get_user(user_id, include_deleted=include_deleted)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    dto = user_to_response_dto(user)
    return user_response_dto_to_dict(dto)


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequestDto,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends(),
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_permission(current_user, Permission.CREATE_USER)
    
    user = await user_service.update_user(user_id, request)
    dto = user_to_response_dto(user)
    return user_response_dto_to_dict(dto)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends(),
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_permission(current_user, Permission.DELETE_USER)
    
    await user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/restore")
async def restore_user(
    user_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(),
    user_service: UserService = Depends(),
):
    current_user = await extract_current_user_from_token(credentials, auth_service)
    if current_user.role != Role.GLOBAL_ADMIN:
        raise HTTPException(status_code=403, detail="Global admin required")
    
    user = await user_service.restore_user(user_id)
    dto = user_to_response_dto(user)
    return user_response_dto_to_dict(dto)
