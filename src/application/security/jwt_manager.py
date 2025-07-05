import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from uuid import UUID
from typing import Optional
from src.application.dtos.auth_dtos import TokenPayload
from src.domain.enums.role import Role


class SecurityConfig:
    """Security configuration constants"""
    SECRET_KEY = "your-secret-key-change-in-production"  # Should be from environment
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days


class PasswordSecurity:
    """Password hashing and verification utilities"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class JWTManager:
    """JWT token management utilities"""
    
    @staticmethod
    def create_access_token(user_id: UUID, username: str, role: Role) -> str:
        """Create an access token"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "user_id": str(user_id),
            "username": username,
            "role": role.value,
            "exp": expire,
            "iat": now,
            "token_type": "access"
        }
        
        return jwt.encode(payload, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM)
    
    @staticmethod
    def create_refresh_token(user_id: UUID, username: str, role: Role) -> str:
        """Create a refresh token"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=SecurityConfig.REFRESH_TOKEN_EXPIRE_DAYS)
        
        payload = {
            "user_id": str(user_id),
            "username": username,
            "role": role.value,
            "exp": expire,
            "iat": now,
            "token_type": "refresh"
        }
        
        return jwt.encode(payload, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenPayload]:
        """Decode and validate a JWT token"""
        try:
            payload = jwt.decode(token, SecurityConfig.SECRET_KEY, algorithms=[SecurityConfig.ALGORITHM])
            
            return TokenPayload(
                user_id=UUID(payload["user_id"]),
                username=payload["username"],
                role=Role(payload["role"]),
                exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
                iat=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
                token_type=payload["token_type"]
            )
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Token is invalid
    
    @staticmethod
    def is_token_expired(token_payload: TokenPayload) -> bool:
        """Check if a token is expired"""
        return datetime.now(timezone.utc) >= token_payload.exp
