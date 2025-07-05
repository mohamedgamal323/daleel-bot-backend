import pytest
from uuid import uuid4, UUID
from src.application.services.category_service import CategoryService
from src.application.dtos.category_dtos import CreateCategoryRequestDto, UpdateCategoryRequestDto
from src.infrastructure_persistence.memory_category_repo import MemoryCategoryRepository
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_create_and_list_category():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="Programming", domain_id=domain_id)
    category = await service.create_category(create_dto)
    
    categories = await service.list_categories(domain_id)
    assert len(categories) == 1
    assert categories[0].name == "Programming"
    assert categories[0].domain_id == domain_id
    assert categories[0].id == category.id
    assert not categories[0].is_deleted()


@pytest.mark.asyncio
async def test_get_category():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="Database", domain_id=domain_id)
    category = await service.create_category(create_dto)
    
    retrieved = await service.get_category(category.id)
    assert retrieved is not None
    assert retrieved.name == "Database"
    assert retrieved.domain_id == domain_id
    
    # Test non-existent category
    non_existent = await service.get_category(uuid4())
    assert non_existent is None


@pytest.mark.asyncio
async def test_get_category_by_name():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="Networking", domain_id=domain_id)
    category = await service.create_category(create_dto)
    
    retrieved = await service.get_category_by_name("Networking", domain_id)
    assert retrieved is not None
    assert retrieved.id == category.id


@pytest.mark.asyncio
async def test_update_category():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    new_domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="Security", domain_id=domain_id)
    category = await service.create_category(create_dto)
    
    # Update name
    update_dto = UpdateCategoryRequestDto(name="Cybersecurity")
    updated = await service.update_category(category.id, update_dto)
    assert updated.name == "Cybersecurity"
    assert updated.domain_id == domain_id
    
    # Update domain
    update_dto = UpdateCategoryRequestDto(domain_id=new_domain_id)
    updated = await service.update_category(category.id, update_dto)
    assert updated.name == "Cybersecurity"
    assert updated.domain_id == new_domain_id


@pytest.mark.asyncio
async def test_list_categories_across_domains():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain1 = uuid4()
    domain2 = uuid4()
    
    # Create categories in different domains
    create_dto1 = CreateCategoryRequestDto(name="Frontend", domain_id=domain1)
    cat1 = await service.create_category(create_dto1)
    create_dto2 = CreateCategoryRequestDto(name="Backend", domain_id=domain1)
    cat2 = await service.create_category(create_dto2)
    create_dto3 = CreateCategoryRequestDto(name="Mobile", domain_id=domain2)
    cat3 = await service.create_category(create_dto3)
    
    # Test domain-specific listing
    domain1_cats = await service.list_categories(domain1)
    assert len(domain1_cats) == 2
    
    domain2_cats = await service.list_categories(domain2)
    assert len(domain2_cats) == 1
    
    # Test listing all categories
    all_cats = await service.list_all_categories()
    assert len(all_cats) == 3


@pytest.mark.asyncio
async def test_delete_and_restore_category():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="DevOps", domain_id=domain_id)
    category = await service.create_category(create_dto)
    
    # Soft delete category
    await service.delete_category(category.id)
    
    # Category should not appear in normal list
    categories = await service.list_categories(domain_id)
    assert len(categories) == 0
    
    # Category should appear in list with deleted
    categories_with_deleted = await service.list_categories(domain_id, include_deleted=True)
    assert len(categories_with_deleted) == 1
    assert categories_with_deleted[0].is_deleted()
    
    # Restore category
    restored = await service.restore_category(category.id)
    assert not restored.is_deleted()
    
    # Category should appear in normal list again
    categories = await service.list_categories(domain_id)
    assert len(categories) == 1


@pytest.mark.asyncio
async def test_duplicate_category_name_in_domain():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain_id = uuid4()
    
    create_dto = CreateCategoryRequestDto(name="Testing", domain_id=domain_id)
    await service.create_category(create_dto)
    
    # Should raise exception for duplicate name in same domain
    with pytest.raises(HTTPException) as exc_info:
        duplicate_dto = CreateCategoryRequestDto(name="Testing", domain_id=domain_id)
        await service.create_category(duplicate_dto)
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_same_category_name_different_domains():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    domain1 = uuid4()
    domain2 = uuid4()
    
    # Should allow same name in different domains
    create_dto1 = CreateCategoryRequestDto(name="AI", domain_id=domain1)
    cat1 = await service.create_category(create_dto1)
    create_dto2 = CreateCategoryRequestDto(name="AI", domain_id=domain2)
    cat2 = await service.create_category(create_dto2)
    
    assert cat1.name == cat2.name
    assert cat1.domain_id != cat2.domain_id
    assert cat1.id != cat2.id


@pytest.mark.asyncio
async def test_category_not_found_errors():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)
    
    non_existent_id = uuid4()
    
    # Update non-existent category
    with pytest.raises(HTTPException) as exc_info:
        update_dto = UpdateCategoryRequestDto(name="new_name")
        await service.update_category(non_existent_id, update_dto)
    assert exc_info.value.status_code == 404
    
    # Delete non-existent category
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_category(non_existent_id)
    assert exc_info.value.status_code == 404
    
    # Restore non-existent category
    with pytest.raises(HTTPException) as exc_info:
        await service.restore_category(non_existent_id)
    assert exc_info.value.status_code == 404
