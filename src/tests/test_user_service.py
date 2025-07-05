import pytest
from uuid import UUID
from src.application.services.user_service import UserService
from src.application.dtos.user_dtos import CreateUserRequestDto, UpdateUserRequestDto
from src.domain.enums.role import Role
from src.infrastructure_persistence.memory_user_repo import MemoryUserRepository
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_and_list_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    create_dto = CreateUserRequestDto(username="alice", role=Role.USER)
    user = await service.create_user(create_dto)
    
    users = await service.list_users()
    assert len(users) == 1
    assert users[0].username == "alice"
    assert users[0].role == Role.USER
    assert users[0].id == user.id
    assert not users[0].is_deleted()


@pytest.mark.asyncio
async def test_get_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    create_dto = CreateUserRequestDto(username="bob", role=Role.GLOBAL_ADMIN)
    user = await service.create_user(create_dto)
    
    retrieved = await service.get_user(user.id)
    assert retrieved is not None
    assert retrieved.username == "bob"
    assert retrieved.role == Role.GLOBAL_ADMIN
    
    # Test non-existent user
    from uuid import uuid4
    non_existent = await service.get_user(uuid4())
    assert non_existent is None


@pytest.mark.asyncio
async def test_update_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    create_dto = CreateUserRequestDto(username="charlie", role=Role.USER)
    user = await service.create_user(create_dto)
    
    # Update username
    update_dto = UpdateUserRequestDto(username="charlie_updated")
    updated = await service.update_user(user.id, update_dto)
    assert updated.username == "charlie_updated"
    assert updated.role == Role.USER
    
    # Update role
    update_dto = UpdateUserRequestDto(role=Role.DOMAIN_ADMIN)
    updated = await service.update_user(user.id, update_dto)
    assert updated.username == "charlie_updated"
    assert updated.role == Role.DOMAIN_ADMIN


@pytest.mark.asyncio
async def test_delete_and_restore_user():
    repo = MemoryUserRepository()
    service = UserService(repo)
    create_dto = CreateUserRequestDto(username="dave", role=Role.USER)
    user = await service.create_user(create_dto)
    
    # Soft delete user
    await service.delete_user(user.id)
    
    # User should not appear in normal list
    users = await service.list_users()
    assert len(users) == 0
    
    # User should appear in list with deleted
    users_with_deleted = await service.list_users(include_deleted=True)
    assert len(users_with_deleted) == 1
    assert users_with_deleted[0].is_deleted()
    
    # Restore user
    restored = await service.restore_user(user.id)
    assert not restored.is_deleted()
    
    # User should appear in normal list again
    users = await service.list_users()
    assert len(users) == 1


@pytest.mark.asyncio
async def test_duplicate_username():
    repo = MemoryUserRepository()
    service = UserService(repo)
    
    create_dto = CreateUserRequestDto(username="duplicate", role=Role.USER)
    await service.create_user(create_dto)
    
    # Should raise exception for duplicate username
    with pytest.raises(HTTPException) as exc_info:
        duplicate_dto = CreateUserRequestDto(username="duplicate", role=Role.GLOBAL_ADMIN)
        await service.create_user(duplicate_dto)
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_user_not_found_errors():
    repo = MemoryUserRepository()
    service = UserService(repo)
    
    from uuid import uuid4
    non_existent_id = uuid4()
    
    # Update non-existent user
    with pytest.raises(HTTPException) as exc_info:
        update_dto = UpdateUserRequestDto(username="new_name")
        await service.update_user(non_existent_id, update_dto)
    assert exc_info.value.status_code == 404
    
    # Delete non-existent user
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_user(non_existent_id)
    assert exc_info.value.status_code == 404
    
    # Restore non-existent user
    with pytest.raises(HTTPException) as exc_info:
        await service.restore_user(non_existent_id)
    assert exc_info.value.status_code == 404
