from fastapi import Depends
from src.domain.persistence.user_repository import UserRepository
from src.domain.persistence.dependencies import get_user_repository


class AuthService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self._user_repo = user_repo

    def authenticate(self, user_id):
        return self._user_repo.get(user_id)
