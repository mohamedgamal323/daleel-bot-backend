from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from src.domain.entities.asset import Asset
from src.domain.enums.asset_type import AssetType
from src.domain.persistence.asset_repository import AssetRepository
from .database.mongodb import get_database


class MongoAssetRepository(AssetRepository):
    def __init__(self):
        self._collection: AsyncIOMotorCollection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            db = get_database()
            self._collection = db.assets
        return self._collection

    async def add(self, asset: Asset) -> None:
        """Add an asset to the database"""
        asset_doc = {
            "_id": str(asset.id),
            "name": asset.name,
            "domain_id": str(asset.domain_id),
            "asset_type": asset.asset_type.value,
            "content": asset.content,
            "category_id": str(asset.category_id) if asset.category_id else None
        }
        await self.collection.insert_one(asset_doc)

    async def get(self, asset_id: UUID) -> Asset | None:
        """Get an asset by ID"""
        asset_doc = await self.collection.find_one({"_id": str(asset_id)})
        if asset_doc:
            return Asset(
                id=UUID(asset_doc["_id"]),
                name=asset_doc["name"],
                domain_id=UUID(asset_doc["domain_id"]),
                asset_type=AssetType(asset_doc["asset_type"]),
                content=asset_doc.get("content"),
                category_id=UUID(asset_doc["category_id"]) if asset_doc.get("category_id") else None
            )
        return None

    async def list(self, domain_id: UUID) -> List[Asset]:
        """List all assets for a domain"""
        assets = []
        async for asset_doc in self.collection.find({"domain_id": str(domain_id)}):
            assets.append(Asset(
                id=UUID(asset_doc["_id"]),
                name=asset_doc["name"],
                domain_id=UUID(asset_doc["domain_id"]),
                asset_type=AssetType(asset_doc["asset_type"]),
                content=asset_doc.get("content"),
                category_id=UUID(asset_doc["category_id"]) if asset_doc.get("category_id") else None
            ))
        return assets

    async def list_by_category(self, category_id: UUID) -> List[Asset]:
        """List all assets for a category"""
        assets = []
        async for asset_doc in self.collection.find({"category_id": str(category_id)}):
            assets.append(Asset(
                id=UUID(asset_doc["_id"]),
                name=asset_doc["name"],
                domain_id=UUID(asset_doc["domain_id"]),
                asset_type=AssetType(asset_doc["asset_type"]),
                content=asset_doc.get("content"),
                category_id=UUID(asset_doc["category_id"]) if asset_doc.get("category_id") else None
            ))
        return assets

    async def update(self, asset: Asset) -> None:
        """Update an existing asset"""
        asset_doc = {
            "name": asset.name,
            "domain_id": str(asset.domain_id),
            "asset_type": asset.asset_type.value,
            "content": asset.content,
            "category_id": str(asset.category_id) if asset.category_id else None
        }
        await self.collection.update_one(
            {"_id": str(asset.id)},
            {"$set": asset_doc}
        )

    async def delete(self, asset_id: UUID) -> None:
        """Delete an asset by ID"""
        await self.collection.delete_one({"_id": str(asset_id)})
