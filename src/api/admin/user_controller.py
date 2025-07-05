from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from src.application.services.user_service import UserService
from src.domain.enums.role import Role
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["admin-users"])


class CreateUserRequest(BaseModel):
    username: str
    role: Role


class UpdateUserRequest(BaseModel):
    username: str | None = None
    role: Role | None = None


def user_response(user):
    return {
        "id": str(user.id),
        "username": user.username,
        "role": user.role.value,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
        "is_deleted": user.is_deleted(),
    }


@router.post("/")
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(),
):
    user = await service.create_user(username=request.username, role=request.role)
    return user_response(user)


@router.get("/")
async def list_all_users(
    include_deleted: bool = Query(True, description="Include soft-deleted users (admin default: true)"),
    service: UserService = Depends()
):
    users = await service.list_users(include_deleted=include_deleted)
    return [user_response(u) for u in users]


@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    include_deleted: bool = Query(True, description="Include soft-deleted user (admin default: true)"),
    service: UserService = Depends()
):
    user = await service.get_user(user_id, include_deleted=include_deleted)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_response(user)


@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    service: UserService = Depends(),
):
    user = await service.update_user(user_id, username=request.username, role=request.role)
    return user_response(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(),
):
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/restore")
async def restore_user(
    user_id: UUID,
    service: UserService = Depends(),
):
    user = await service.restore_user(user_id)
    return user_response(user)
