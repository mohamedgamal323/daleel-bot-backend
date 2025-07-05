import pytest
from uuid import UUID
from src.application.services.domain_service import DomainService
from src.application.dtos.domain_dtos import CreateDomainRequestDto, UpdateDomainRequestDto
from src.infrastructure_persistence.memory_domain_repo import MemoryDomainRepository
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_and_list_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    create_dto = CreateDomainRequestDto(name="education")
    domain = await service.create_domain(create_dto)
    
    domains = await service.list_domains()
    assert len(domains) == 1
    assert domains[0].name == "education"
    assert domains[0].id == domain.id
    assert not domains[0].is_deleted()


@pytest.mark.asyncio
async def test_get_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    create_dto = CreateDomainRequestDto(name="technology")
    domain = await service.create_domain(create_dto)
    
    retrieved = await service.get_domain(domain.id)
    assert retrieved is not None
    assert retrieved.name == "technology"
    
    # Test non-existent domain
    from uuid import uuid4
    non_existent = await service.get_domain(uuid4())
    assert non_existent is None


@pytest.mark.asyncio
async def test_get_domain_by_name():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    create_dto = CreateDomainRequestDto(name="healthcare")
    domain = await service.create_domain(create_dto)
    
    retrieved = await service.get_domain_by_name("healthcare")
    assert retrieved is not None
    assert retrieved.id == domain.id


@pytest.mark.asyncio
async def test_update_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    create_dto = CreateDomainRequestDto(name="science")
    domain = await service.create_domain(create_dto)
    
    update_dto = UpdateDomainRequestDto(name="medical_science")
    updated = await service.update_domain(domain.id, update_dto)
    assert updated.name == "medical_science"
    assert updated.id == domain.id


@pytest.mark.asyncio
async def test_delete_and_restore_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    create_dto = CreateDomainRequestDto(name="finance")
    domain = await service.create_domain(create_dto)
    
    # Soft delete domain
    await service.delete_domain(domain.id)
    
    # Domain should not appear in normal list
    domains = await service.list_domains()
    assert len(domains) == 0
    
    # Domain should appear in list with deleted
    domains_with_deleted = await service.list_domains(include_deleted=True)
    assert len(domains_with_deleted) == 1
    assert domains_with_deleted[0].is_deleted()
    
    # Restore domain
    restored = await service.restore_domain(domain.id)
    assert not restored.is_deleted()
    
    # Domain should appear in normal list again
    domains = await service.list_domains()
    assert len(domains) == 1


@pytest.mark.asyncio
async def test_duplicate_domain_name():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    
    create_dto = CreateDomainRequestDto(name="duplicate_domain")
    await service.create_domain(create_dto)
    
    # Should raise exception for duplicate name
    with pytest.raises(HTTPException) as exc_info:
        duplicate_dto = CreateDomainRequestDto(name="duplicate_domain")
        await service.create_domain(duplicate_dto)
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_domain_not_found_errors():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    
    from uuid import uuid4
    non_existent_id = uuid4()
    
    # Update non-existent domain
    with pytest.raises(HTTPException) as exc_info:
        update_dto = UpdateDomainRequestDto(name="new_name")
        await service.update_domain(non_existent_id, update_dto)
    assert exc_info.value.status_code == 404
    
    # Delete non-existent domain
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_domain(non_existent_id)
    assert exc_info.value.status_code == 404
    
    # Restore non-existent domain
    with pytest.raises(HTTPException) as exc_info:
        await service.restore_domain(non_existent_id)
    assert exc_info.value.status_code == 404
