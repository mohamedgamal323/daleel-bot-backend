from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timezone
from ..enums.role import Role


@dataclass
class TokenPayload:
    """JWT token payload structure"""
    user_id: UUID
    username: str
    role: Role
    exp: datetime
    iat: datetime
    token_type: str  # 'access' or 'refresh'


@dataclass
class LoginCredentials:
    """User login credentials"""
    username: str
    password: str


@dataclass
class LoginResponse:
    """Response after successful login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # Access token expiry in seconds
    user: dict = None  # User information


@dataclass
class TokenRefreshRequest:
    """Request to refresh access token"""
    refresh_token: str


@dataclass
class ChangePasswordRequest:
    """Request to change user password"""
    current_password: str
    new_password: str


@dataclass
class ResetPasswordRequest:
    """Request to reset password (admin only)"""
    new_password: str
