from fastapi import APIRouter, Depends
from src.app.application.services.user_service import UserService
from src.app.infrastructure.repositories.memory_user_repo import MemoryUserRepository
from src.app.domain.enums.role import Role

router = APIRouter(prefix="/users", tags=["users"])


def get_repo() -> MemoryUserRepository:
    return MemoryUserRepository()


def get_service(repo: MemoryUserRepository = Depends(get_repo)) -> UserService:
    return UserService(repo)


@router.post("/")
async def create_user(
    username: str,
    role: Role,
    service: UserService = Depends(get_service),
):
    user = service.create_user(username=username, role=role)
    return {"id": str(user.id), "username": user.username}


@router.get("/")
async def list_users(service: UserService = Depends(get_service)):
    users = service.list_users()
    return [{"id": str(u.id), "username": u.username} for u in users]
