from fastapi import APIRouter, Depends
from src.application.services.user_service import UserService
from src.common.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["admin-users"])


@router.get("/")
async def list_all_users(service: UserService = Depends(get_user_service)):
    users = await service.list_users()
    return [{"id": str(u.id), "username": u.username, "role": u.role.value} for u in users]
