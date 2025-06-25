from typing import Iterable
from ..interfaces.user_repository import UserRepository
from ...domain.entities.user import User
from ...domain.enums.role import Role


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def create_user(self, username: str, role: Role) -> User:
        user = User(username=username, role=role)
        self._repo.add(user)
        return user

    def list_users(self) -> Iterable[User]:
        return self._repo.list()
