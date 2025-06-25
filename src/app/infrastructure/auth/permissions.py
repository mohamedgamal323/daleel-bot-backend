from ..repositories.memory_user_repo import MemoryUserRepository
from ...domain.enums.role import Role


def has_role(user_id, role: Role, user_repo: MemoryUserRepository) -> bool:
    user = user_repo.get(user_id)
    return user is not None and user.role == role
