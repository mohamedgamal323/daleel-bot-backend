from src.app.application.services.user_service import UserService
from src.app.domain.enums.role import Role
from src.app.infrastructure.repositories.memory_user_repo import MemoryUserRepository


def test_create_and_list_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    service.create_user("alice", Role.USER)
    users = list(service.list_users())
    assert len(users) == 1
    assert users[0].username == "alice"
