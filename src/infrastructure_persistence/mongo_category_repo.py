from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from src.domain.entities.category import Category
from src.domain.persistence.category_repository import CategoryRepository
from .database.mongodb import get_database


class MongoCategoryRepository(CategoryRepository):
    def __init__(self):
        self._collection: AsyncIOMotorCollection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            db = get_database()
            self._collection = db.categories
        return self._collection

    async def add(self, category: Category) -> None:
        """Add a category to the database"""
        category_doc = {
            "_id": str(category.id),
            "name": category.name,
            "domain_id": str(category.domain_id)
        }
        await self.collection.insert_one(category_doc)

    async def get(self, category_id: UUID) -> Category | None:
        """Get a category by ID"""
        category_doc = await self.collection.find_one({"_id": str(category_id)})
        if category_doc:
            return Category(
                id=UUID(category_doc["_id"]),
                name=category_doc["name"],
                domain_id=UUID(category_doc["domain_id"])
            )
        return None

    async def get_by_name(self, name: str, domain_id: UUID) -> Category | None:
        """Get a category by name within a domain"""
        category_doc = await self.collection.find_one({
            "name": name,
            "domain_id": str(domain_id)
        })
        if category_doc:
            return Category(
                id=UUID(category_doc["_id"]),
                name=category_doc["name"],
                domain_id=UUID(category_doc["domain_id"])
            )
        return None

    async def list(self, domain_id: UUID) -> List[Category]:
        """List all categories for a domain"""
        categories = []
        async for category_doc in self.collection.find({"domain_id": str(domain_id)}):
            categories.append(Category(
                id=UUID(category_doc["_id"]),
                name=category_doc["name"],
                domain_id=UUID(category_doc["domain_id"])
            ))
        return categories

    async def list_all(self) -> List[Category]:
        """List all categories"""
        categories = []
        async for category_doc in self.collection.find():
            categories.append(Category(
                id=UUID(category_doc["_id"]),
                name=category_doc["name"],
                domain_id=UUID(category_doc["domain_id"])
            ))
        return categories

    async def update(self, category: Category) -> None:
        """Update an existing category"""
        category_doc = {
            "name": category.name,
            "domain_id": str(category.domain_id)
        }
        await self.collection.update_one(
            {"_id": str(category.id)},
            {"$set": category_doc}
        )

    async def delete(self, category_id: UUID) -> None:
        """Delete a category by ID"""
        await self.collection.delete_one({"_id": str(category_id)})
