from src.domain.persistence.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def authenticate(self, user_id):
        return self._user_repo.get(user_id)
