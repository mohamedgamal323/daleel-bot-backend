from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
from src.common.config import get_settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Connect to MongoDB database"""
    settings = get_settings()
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb.database = mongodb.client[settings.MONGODB_DATABASE]
        
        # Test the connection
        await mongodb.client.admin.command('ismaster')
        logger.info(f"Connected to MongoDB database: {settings.MONGODB_DATABASE}")
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if mongodb.client:
        mongodb.client.close()
        logger.info("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance"""
    return mongodb.database
