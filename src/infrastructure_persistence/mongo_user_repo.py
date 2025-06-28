from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorCollection
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.persistence.user_repository import UserRepository
from .database.mongodb import get_database


class MongoUserRepository(UserRepository):
    def __init__(self):
        self._collection: AsyncIOMotorCollection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            db = get_database()
            self._collection = db.users
        return self._collection

    async def add(self, user: User) -> None:
        """Add a user to the database"""
        user_doc = {
            "_id": str(user.id),
            "username": user.username,
            "role": user.role.value
        }
        await self.collection.insert_one(user_doc)

    async def get(self, user_id: UUID) -> User | None:
        """Get a user by ID"""
        user_doc = await self.collection.find_one({"_id": str(user_id)})
        if user_doc:
            return User(
                id=UUID(user_doc["_id"]),
                username=user_doc["username"],
                role=Role(user_doc["role"])
            )
        return None

    async def get_by_username(self, username: str) -> User | None:
        """Get a user by username"""
        user_doc = await self.collection.find_one({"username": username})
        if user_doc:
            return User(
                id=UUID(user_doc["_id"]),
                username=user_doc["username"],
                role=Role(user_doc["role"])
            )
        return None

    async def list(self) -> List[User]:
        """List all users"""
        users = []
        async for user_doc in self.collection.find():
            users.append(User(
                id=UUID(user_doc["_id"]),
                username=user_doc["username"],
                role=Role(user_doc["role"])
            ))
        return users

    async def update(self, user: User) -> None:
        """Update an existing user"""
        user_doc = {
            "username": user.username,
            "role": user.role.value
        }
        await self.collection.update_one(
            {"_id": str(user.id)},
            {"$set": user_doc}
        )

    async def delete(self, user_id: UUID) -> None:
        """Delete a user by ID"""
        await self.collection.delete_one({"_id": str(user_id)})
