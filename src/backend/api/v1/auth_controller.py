from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from src.backend.application.dtos.auth_dtos import (
    LoginCredentials, LoginResponse, TokenRefreshRequest,
    ChangePasswordRequest, ResetPasswordRequest, UserRegistrationRequest
)
from src.backend.domain.entities.user import User
from src.backend.domain.enums.role import Role
from src.backend.application.services.auth_service import AuthService
from src.backend.application.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["authentication"])

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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def validate_global_admin(user: User) -> None:
    """Helper function to validate global admin role"""
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    if user.role != Role.GLOBAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Global admin required."
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginCredentials,
    auth_service: AuthService = Depends()
):
    """User login endpoint"""
    return await auth_service.login(credentials)


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request: TokenRefreshRequest,
    auth_service: AuthService = Depends()
):
    """Refresh access token using refresh token"""
    return await auth_service.refresh_token(request)


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends()
):
    """Change current user's password"""
    current_user = await extract_current_user_from_token(credentials, auth_service)
    
    success = await auth_service.change_password(current_user.id, request)
    if success:
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to change password"
        )


@router.post("/admin/reset-password/{user_id}")
async def reset_password_admin(
    user_id: UUID,
    request: ResetPasswordRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends()
):
    """Reset user password (admin only)"""
    current_user = await extract_current_user_from_token(credentials, auth_service)
    validate_global_admin(current_user)
    
    success = await auth_service.reset_password_admin(user_id, request)
    if success:
        return {"message": "Password reset successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reset password"
        )


@router.get("/me")
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends()
):
    """Get current user information"""
    current_user = await extract_current_user_from_token(credentials, auth_service)
    
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None
    }


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends()
):
    """User logout endpoint (client should discard tokens)"""
    # Validate the token (this ensures it's a valid authenticated request)
    await extract_current_user_from_token(credentials, auth_service)
    
    # In a real implementation, you might want to blacklist the token
    # For now, we just return a success message
    return {"message": "Logged out successfully. Please discard your tokens."}


@router.post("/register")
async def register_user(
    request: UserRegistrationRequest,
    user_service: UserService = Depends()
):
    """User registration endpoint"""
    from src.backend.application.security.jwt_manager import PasswordSecurity
    from src.backend.application.dtos.user_dtos import UserRegistrationDto
    
    # Hash the password
    hashed_password = PasswordSecurity.hash_password(request.password)
    
    # Create registration DTO
    registration_dto = UserRegistrationDto(
        username=request.username,
        email=request.email,
        password_hash=hashed_password,
        role=request.role
    )
    
    # Register user through the service
    user = await user_service.register_user(registration_dto)
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active
        }
    }
