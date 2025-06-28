from fastapi import APIRouter, Depends
from src.application.services.user_service import UserService
from src.domain.enums.role import Role

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(
    username: str,
    role: Role,
    service: UserService = Depends(),
):
    user = await service.create_user(username=username, role=role)
    return {"id": str(user.id), "username": user.username, "role": user.role.value}


@router.get("/")
async def list_users(service: UserService = Depends()):
    users = await service.list_users()
    return [{"id": str(u.id), "username": u.username, "role": u.role.value} for u in users]
