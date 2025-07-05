from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from src.domain.persistence.category_repository import CategoryRepository
from src.domain.entities.category import Category
from src.domain.persistence.dependencies import get_category_repository
from src.application.dtos.category_dtos import CreateCategoryRequestDto, UpdateCategoryRequestDto


class CategoryService:
    def __init__(self, repo: CategoryRepository = Depends(get_category_repository)):
        self._repo = repo

    async def create_category(self, dto: CreateCategoryRequestDto) -> Category:
        # Check if category already exists in this domain
        existing = await self._repo.get_by_name(dto.name, dto.domain_id, include_deleted=True)
        if existing and not existing.is_deleted():
            raise HTTPException(status_code=400, detail="Category with this name already exists in this domain")
        
        category = Category(name=dto.name, domain_id=dto.domain_id)
        await self._repo.add(category)
        return category

    async def get_category(self, category_id: UUID, include_deleted: bool = False) -> Category | None:
        return await self._repo.get(category_id, include_deleted=include_deleted)

    async def get_category_by_name(self, name: str, domain_id: UUID, include_deleted: bool = False) -> Category | None:
        return await self._repo.get_by_name(name, domain_id, include_deleted=include_deleted)

    async def list_categories(self, domain_id: UUID, include_deleted: bool = False) -> List[Category]:
        return await self._repo.list(domain_id, include_deleted=include_deleted)

    async def list_all_categories(self, include_deleted: bool = False) -> List[Category]:
        return await self._repo.list_all(include_deleted=include_deleted)

    async def update_category(self, category_id: UUID, dto: UpdateCategoryRequestDto) -> Category:
        category = await self._repo.get(category_id, include_deleted=False)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Check if new name conflicts with existing category in the domain
        target_domain_id = dto.domain_id or category.domain_id
        if dto.name and (dto.name != category.name or dto.domain_id != category.domain_id):
            existing = await self._repo.get_by_name(dto.name, target_domain_id, include_deleted=True)
            if existing and not existing.is_deleted() and existing.id != category_id:
                raise HTTPException(status_code=400, detail="Category with this name already exists in this domain")
            category.name = dto.name
        
        if dto.domain_id:
            category.domain_id = dto.domain_id
        
        await self._repo.update(category)
        return category

    async def delete_category(self, category_id: UUID) -> None:
        category = await self._repo.get(category_id, include_deleted=False)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        await self._repo.soft_delete(category_id)

    async def restore_category(self, category_id: UUID) -> Category:
        category = await self._repo.get(category_id, include_deleted=True)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        if not category.is_deleted():
            raise HTTPException(status_code=400, detail="Category is not deleted")
        
        await self._repo.restore(category_id)
        return await self._repo.get(category_id, include_deleted=False)
