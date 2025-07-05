"""Domain persistence dependencies - repository providers"""

from fastapi import Depends
from src.common.config import get_settings
from .user_repository import UserRepository
from .domain_repository import DomainRepository  
from .category_repository import CategoryRepository
from .asset_repository import AssetRepository

# Singleton instances for memory repositories
_user_repo_instance = None
_domain_repo_instance = None
_category_repo_instance = None
_asset_repo_instance = None


def get_user_repository() -> UserRepository:
    """Get user repository implementation based on configuration"""
    global _user_repo_instance
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_user_repo import MongoUserRepository
        return MongoUserRepository()
    else:
        if _user_repo_instance is None:
            from src.infrastructure_persistence.memory_user_repo import MemoryUserRepository
            _user_repo_instance = MemoryUserRepository()
        return _user_repo_instance


def get_domain_repository() -> DomainRepository:
    """Get domain repository implementation based on configuration"""
    global _domain_repo_instance
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_domain_repo import MongoDomainRepository
        return MongoDomainRepository()
    else:
        if _domain_repo_instance is None:
            from src.infrastructure_persistence.memory_domain_repo import MemoryDomainRepository
            _domain_repo_instance = MemoryDomainRepository()
        return _domain_repo_instance


def get_category_repository() -> CategoryRepository:
    """Get category repository implementation based on configuration"""
    global _category_repo_instance
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_category_repo import MongoCategoryRepository
        return MongoCategoryRepository()
    else:
        if _category_repo_instance is None:
            from src.infrastructure_persistence.memory_category_repo import MemoryCategoryRepository
            _category_repo_instance = MemoryCategoryRepository()
        return _category_repo_instance


def get_asset_repository() -> AssetRepository:
    """Get asset repository implementation based on configuration"""
    global _asset_repo_instance
    settings = get_settings()
    if getattr(settings, 'USE_MONGODB', False):
        from src.infrastructure_persistence.mongo_asset_repo import MongoAssetRepository
        return MongoAssetRepository()
    else:
        if _asset_repo_instance is None:
            from src.infrastructure_persistence.memory_asset_repo import MemoryAssetRepository
            _asset_repo_instance = MemoryAssetRepository()
        return _asset_repo_instance


# Domain persistence exports
__all__ = [
    "get_user_repository",
    "get_domain_repository", 
    "get_category_repository",
    "get_asset_repository",
]
