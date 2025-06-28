import pytest
from src.application.services.user_service import UserService
from src.domain.enums.role import Role
from src.infrastructure_persistence.memory_user_repo import MemoryUserRepository


@pytest.mark.asyncio
async def test_create_and_list_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    await service.create_user("alice", Role.USER)
    users = await service.list_users()
    assert len(users) == 1
    assert users[0].username == "alice"
