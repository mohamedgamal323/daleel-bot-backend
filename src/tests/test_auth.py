import pytest
from src.application.security.jwt_manager import PasswordSecurity, JWTManager
from src.domain.enums.role import Role
from uuid import uuid4


def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password123"
    
    # Hash password
    hashed = PasswordSecurity.hash_password(password)
    assert hashed != password
    assert len(hashed) > 50  # bcrypt hashes are long
    
    # Verify correct password
    assert PasswordSecurity.verify_password(password, hashed) is True
    
    # Verify incorrect password
    assert PasswordSecurity.verify_password("wrong_password", hashed) is False


def test_jwt_token_creation_and_validation():
    """Test JWT token creation and validation"""
    user_id = uuid4()
    username = "test_user"
    role = Role.USER
    
    # Create access token
    access_token = JWTManager.create_access_token(user_id, username, role)
    assert isinstance(access_token, str)
    assert len(access_token) > 50
    
    # Create refresh token  
    refresh_token = JWTManager.create_refresh_token(user_id, username, role)
    assert isinstance(refresh_token, str)
    assert len(refresh_token) > 50
    
    # Decode and validate access token
    payload = JWTManager.decode_token(access_token)
    assert payload is not None
    assert payload.user_id == user_id
    assert payload.username == username
    assert payload.role == role
    assert payload.token_type == "access"
    
    # Decode and validate refresh token
    payload = JWTManager.decode_token(refresh_token)
    assert payload is not None
    assert payload.user_id == user_id
    assert payload.username == username
    assert payload.role == role
    assert payload.token_type == "refresh"


def test_invalid_token():
    """Test invalid token handling"""
    # Test with invalid token
    payload = JWTManager.decode_token("invalid.token.here")
    assert payload is None
    
    # Test with empty token
    payload = JWTManager.decode_token("")
    assert payload is None
