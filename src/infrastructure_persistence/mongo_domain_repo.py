from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from src.domain.entities.domain import Domain
from src.domain.persistence.domain_repository import DomainRepository
from .database.mongodb import get_database


class MongoDomainRepository(DomainRepository):
    def __init__(self):
        self._collection: AsyncIOMotorCollection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            db = get_database()
            self._collection = db.domains
        return self._collection

    async def add(self, domain: Domain) -> None:
        """Add a domain to the database"""
        domain_doc = {
            "_id": str(domain.id),
            "name": domain.name
        }
        await self.collection.insert_one(domain_doc)

    async def get(self, domain_id: UUID) -> Domain | None:
        """Get a domain by ID"""
        domain_doc = await self.collection.find_one({"_id": str(domain_id)})
        if domain_doc:
            return Domain(
                id=UUID(domain_doc["_id"]),
                name=domain_doc["name"]
            )
        return None

    async def get_by_name(self, name: str) -> Domain | None:
        """Get a domain by name"""
        domain_doc = await self.collection.find_one({"name": name})
        if domain_doc:
            return Domain(
                id=UUID(domain_doc["_id"]),
                name=domain_doc["name"]
            )
        return None

    async def list(self) -> List[Domain]:
        """List all domains"""
        domains = []
        async for domain_doc in self.collection.find():
            domains.append(Domain(
                id=UUID(domain_doc["_id"]),
                name=domain_doc["name"]
            ))
        return domains

    async def update(self, domain: Domain) -> None:
        """Update an existing domain"""
        domain_doc = {
            "name": domain.name
        }
        await self.collection.update_one(
            {"_id": str(domain.id)},
            {"$set": domain_doc}
        )

    async def delete(self, domain_id: UUID) -> None:
        """Delete a domain by ID"""
        await self.collection.delete_one({"_id": str(domain_id)})
