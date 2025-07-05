from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from src.domain.persistence.domain_repository import DomainRepository
from src.domain.entities.domain import Domain
from src.domain.persistence.dependencies import get_domain_repository
from src.application.dtos.domain_dtos import CreateDomainRequestDto, UpdateDomainRequestDto


class DomainService:
    def __init__(self, repo: DomainRepository = Depends(get_domain_repository)):
        self._repo = repo

    async def create_domain(self, dto: CreateDomainRequestDto) -> Domain:
        # Check if domain already exists
        existing = await self._repo.get_by_name(dto.name, include_deleted=True)
        if existing and not existing.is_deleted():
            raise HTTPException(status_code=400, detail="Domain with this name already exists")
        
        domain = Domain(name=dto.name)
        await self._repo.add(domain)
        return domain

    async def get_domain(self, domain_id: UUID, include_deleted: bool = False) -> Domain | None:
        return await self._repo.get(domain_id, include_deleted=include_deleted)

    async def get_domain_by_name(self, name: str, include_deleted: bool = False) -> Domain | None:
        return await self._repo.get_by_name(name, include_deleted=include_deleted)

    async def list_domains(self, include_deleted: bool = False) -> List[Domain]:
        return await self._repo.list(include_deleted=include_deleted)

    async def update_domain(self, domain_id: UUID, dto: UpdateDomainRequestDto) -> Domain:
        domain = await self._repo.get(domain_id, include_deleted=False)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")
        
        # Check if new name conflicts with existing domain
        if dto.name and dto.name != domain.name:
            existing = await self._repo.get_by_name(dto.name, include_deleted=True)
            if existing and not existing.is_deleted():
                raise HTTPException(status_code=400, detail="Domain with this name already exists")
            domain.name = dto.name
        
        await self._repo.update(domain)
        return domain

    async def delete_domain(self, domain_id: UUID) -> None:
        domain = await self._repo.get(domain_id, include_deleted=False)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")
        
        await self._repo.soft_delete(domain_id)

    async def restore_domain(self, domain_id: UUID) -> Domain:
        domain = await self._repo.get(domain_id, include_deleted=True)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")
        
        if not domain.is_deleted():
            raise HTTPException(status_code=400, detail="Domain is not deleted")
        
        await self._repo.restore(domain_id)
        return await self._repo.get(domain_id, include_deleted=False)
