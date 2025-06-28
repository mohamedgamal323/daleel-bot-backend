"""Domain persistence dependencies - repository providers"""

from fastapi import Depends
from src.common.config import get_settings
from .user_repository import UserRepository
from .domain_repository import DomainRepository  
from .category_repository import CategoryRepository
from .asset_repository import AssetRepository


def get_user_repository() -> UserRepository:
    """Get user repository implementation based on configuration"""
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_user_repo import MongoUserRepository
        return MongoUserRepository()
    else:
        from src.infrastructure_persistence.memory_user_repo import MemoryUserRepository
        return MemoryUserRepository()


def get_domain_repository() -> DomainRepository:
    """Get domain repository implementation based on configuration"""
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_domain_repo import MongoDomainRepository
        return MongoDomainRepository()
    else:
        from src.infrastructure_persistence.memory_domain_repo import MemoryDomainRepository
        return MemoryDomainRepository()


def get_category_repository() -> CategoryRepository:
    """Get category repository implementation based on configuration"""
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_category_repo import MongoCategoryRepository
        return MongoCategoryRepository()
    else:
        from src.infrastructure_persistence.memory_category_repo import MemoryCategoryRepository
        return MemoryCategoryRepository()


def get_asset_repository() -> AssetRepository:
    """Get asset repository implementation based on configuration"""
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_asset_repo import MongoAssetRepository
        return MongoAssetRepository()
    else:
        from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository
        return MemoryAssetRepository()


# Domain persistence exports
__all__ = [
    "get_user_repository",
    "get_domain_repository", 
    "get_category_repository",
    "get_asset_repository",
]
