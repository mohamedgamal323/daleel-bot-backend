from fastapi import APIRouter
from src.app.api.v1.users import service as user_service

router = APIRouter(prefix="/users", tags=["admin-users"])


@router.get("/")
async def list_all_users():
    users = user_service.list_users()
    return [{"id": str(u.id), "username": u.username} for u in users]
