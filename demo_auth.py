#!/usr/bin/env python3
"""
Demo script to showcase the authentication system.
This script demonstrates user registration, login, and protected API access.
"""

import asyncio
import json
from src.application.services.auth_service import AuthService
from src.application.services.user_service import UserService
from src.application.dtos.auth_dtos import LoginCredentials
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.application.security.jwt_manager import PasswordSecurity, JWTManager
from src.infrastructure_persistence.memory_user_repo import MemoryUserRepository
from src.domain.persistence.dependencies import get_user_repository


async def demo_authentication_system():
    """Demonstrate the complete authentication flow"""
    print("=" * 60)
    print("DALEEL BOT AUTHENTICATION SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize repositories and services
    user_repo = MemoryUserRepository()
    auth_service = AuthService(user_repo)
    user_service = UserService(user_repo)
    
    print("\n1. Creating a test user...")
    
    # Create a test user with hashed password
    hashed_password = PasswordSecurity.hash_password("demo_password123")
    test_user = User(
        username="demo_user",
        email="demo@example.com",
        password_hash=hashed_password,
        role=Role.USER,
        is_active=True
    )
    await user_repo.add(test_user)
    print(f"✓ Created user: {test_user.username} ({test_user.role.value})")
    
    # Create an admin user
    admin_password = PasswordSecurity.hash_password("admin_password123")
    admin_user = User(
        username="admin_user",
        email="admin@example.com",
        password_hash=admin_password,
        role=Role.GLOBAL_ADMIN,
        is_active=True
    )
    await user_repo.add(admin_user)
    print(f"✓ Created admin: {admin_user.username} ({admin_user.role.value})")
    
    print("\n2. Testing user login...")
    
    # Test user login
    credentials = LoginCredentials(username="demo_user", password="demo_password123")
    try:
        login_response = await auth_service.login(credentials)
        print(f"✓ Login successful!")
        print(f"  Access Token (first 50 chars): {login_response.access_token[:50]}...")
        print(f"  User ID: {login_response.user['id']}")
        print(f"  Role: {login_response.user['role']}")
        
        # Store token for later use
        user_token = login_response.access_token
        
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return
    
    print("\n3. Testing admin login...")
    
    # Test admin login
    admin_credentials = LoginCredentials(username="admin_user", password="admin_password123")
    try:
        admin_login_response = await auth_service.login(admin_credentials)
        print(f"✓ Admin login successful!")
        print(f"  Role: {admin_login_response.user['role']}")
        
        # Store admin token
        admin_token = admin_login_response.access_token
        
    except Exception as e:
        print(f"✗ Admin login failed: {e}")
        return
    
    print("\n4. Testing token validation...")
    
    # Test token validation
    current_user = await auth_service.get_current_user_from_token(user_token)
    if current_user:
        print(f"✓ Token validation successful for user: {current_user.username}")
    else:
        print("✗ Token validation failed")
    
    print("\n5. Testing permission system...")
    
    from src.domain.enums.permission import get_role_permissions, Permission
    
    # Check user permissions
    user_permissions = get_role_permissions(Role.USER.value)
    print(f"✓ User permissions: {[p.value for p in user_permissions]}")
    
    # Check admin permissions
    admin_permissions = get_role_permissions(Role.GLOBAL_ADMIN.value)
    print(f"✓ Admin permissions: {len(admin_permissions)} total permissions")
    
    # Test specific permission checks
    can_read_assets = Permission.READ_ASSET in user_permissions
    can_create_users = Permission.CREATE_USER in user_permissions
    admin_can_create_users = Permission.CREATE_USER in admin_permissions
    
    print(f"  User can read assets: {can_read_assets}")
    print(f"  User can create users: {can_create_users}")
    print(f"  Admin can create users: {admin_can_create_users}")
    
    print("\n6. Testing token refresh...")
    
    # Test token refresh
    from src.application.dtos.auth_dtos import TokenRefreshRequest
    refresh_request = TokenRefreshRequest(refresh_token=login_response.refresh_token)
    
    try:
        refreshed_response = await auth_service.refresh_token(refresh_request)
        print("✓ Token refresh successful!")
        print(f"  New token (first 50 chars): {refreshed_response.access_token[:50]}...")
    except Exception as e:
        print(f"✗ Token refresh failed: {e}")
    
    print("\n7. Testing password change...")
    
    # Test password change
    from src.application.dtos.auth_dtos import ChangePasswordRequest
    change_request = ChangePasswordRequest(
        current_password="demo_password123",
        new_password="new_demo_password123"
    )
    
    try:
        await auth_service.change_password(test_user.id, change_request)
        print("✓ Password change successful!")
        
        # Test login with new password
        new_credentials = LoginCredentials(username="demo_user", password="new_demo_password123")
        new_login = await auth_service.login(new_credentials)
        print("✓ Login with new password successful!")
        
    except Exception as e:
        print(f"✗ Password change failed: {e}")
    
    print("\n8. Testing invalid scenarios...")
    
    # Test invalid login
    try:
        invalid_credentials = LoginCredentials(username="demo_user", password="wrong_password")
        await auth_service.login(invalid_credentials)
        print("✗ Invalid login should have failed!")
    except Exception:
        print("✓ Invalid login correctly rejected")
    
    # Test invalid token
    invalid_user = await auth_service.get_current_user_from_token("invalid.token.here")
    if invalid_user is None:
        print("✓ Invalid token correctly rejected")
    else:
        print("✗ Invalid token should have been rejected!")
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION SYSTEM DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("• User registration and secure password hashing")
    print("• JWT token creation and validation")
    print("• Role-based access control (RBAC)")
    print("• Permission-based authorization")
    print("• Token refresh mechanism")
    print("• Password change functionality")
    print("• Proper error handling for invalid credentials")
    print("\nThe system is ready for frontend integration!")


if __name__ == "__main__":
    asyncio.run(demo_authentication_system())
