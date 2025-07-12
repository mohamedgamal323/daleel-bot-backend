import pytest
from fastapi.testclient import TestClient
from src.backend.main import create_app
from src.backend.domain.entities.user import User
from src.backend.domain.enums.role import Role
from src.backend.application.security.jwt_manager import PasswordSecurity
from src.backend.infrastructure_persistence.memory_user_repo import MemoryUserRepository


@pytest.fixture
def app():
    """Create test FastAPI app"""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def memory_user_repo():
    """Create memory user repository for testing"""
    return MemoryUserRepository()


@pytest.fixture
async def test_user(memory_user_repo):
    """Create a test user"""
    hashed_password = PasswordSecurity.hash_password("test_password123")
    user = User(
        username="test_user",
        email="test@example.com",
        password=hashed_password,
        role=Role.USER,
        is_active=True
    )
    await memory_user_repo.add(user)
    return user


@pytest.fixture
async def admin_user(memory_user_repo):
    """Create an admin test user"""
    hashed_password = PasswordSecurity.hash_password("admin_password123")
    user = User(
        username="admin_user",
        email="admin@example.com",
        password=hashed_password,
        role=Role.GLOBAL_ADMIN,
        is_active=True
    )
    await memory_user_repo.add(user)
    return user


@pytest.mark.asyncio
async def test_user_registration(client):
    """Test user registration endpoint"""
    registration_data = {
        "username": "new_user",
        "email": "new@example.com",
        "password": "new_password123",
        "role": "user"
    }
    
    response = client.post("/api/v1/auth/register", json=registration_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "new_user"
    assert data["user"]["email"] == "new@example.com"
    assert data["user"]["role"] == "user"


@pytest.mark.asyncio
async def test_user_login_flow(client):
    """Test complete login flow"""
    # First register a user (in a real scenario this would be done via registration)
    registration_data = {
        "username": "login_test_user",
        "email": "login@example.com",
        "password": "test_password123",
        "role": "user"
    }
    
    reg_response = client.post("/api/v1/auth/register", json=registration_data)
    assert reg_response.status_code == 200
    
    # Now test login
    login_data = {
        "username": "login_test_user",
        "password": "test_password123"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "login_test_user"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_protected_endpoint_with_token(client):
    """Test accessing protected endpoint with valid token"""
    # Register and login
    registration_data = {
        "username": "protected_test_user",
        "email": "protected@example.com",
        "password": "test_password123",
        "role": "user"
    }
    
    reg_response = client.post("/api/v1/auth/register", json=registration_data)
    assert reg_response.status_code == 200
    
    login_data = {
        "username": "protected_test_user",
        "password": "test_password123"
    }
    
    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "protected_test_user"


@pytest.mark.asyncio 
async def test_invalid_login_credentials(client):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent_user",
        "password": "wrong_password"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]
