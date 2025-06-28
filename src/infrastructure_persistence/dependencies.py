"""Infrastructure persistence dependencies - concrete repository implementations"""

from typing import Type
from src.domain.persistence.user_repository import UserRepository
from src.domain.persistence.domain_repository import DomainRepository
from src.domain.persistence.category_repository import CategoryRepository
from src.domain.persistence.asset_repository import AssetRepository
from src.common.config import get_settings

from .memory_user_repo import MemoryUserRepository
from .memory_domain_repo import MemoryDomainRepository
from .memory_category_repo import MemoryCategoryRepository
from .memory_asset_repo import MemoryAssetRepository

# Only import MongoDB repositories if needed
_mongo_repos_imported = False


def _ensure_mongo_imports():
    """Lazy import MongoDB repositories only when needed"""
    global _mongo_repos_imported
    if not _mongo_repos_imported:
        global MongoUserRepository, MongoDomainRepository, MongoCategoryRepository, MongoAssetRepository
        from .mongo_user_repo import MongoUserRepository
        from .mongo_domain_repo import MongoDomainRepository
        from .mongo_category_repo import MongoCategoryRepository
        from .mongo_asset_repo import MongoAssetRepository
        _mongo_repos_imported = True


def get_user_repository() -> UserRepository:
    """Get user repository implementation based on configuration"""
    settings = get_settings()
    if settings.USE_MONGODB:
        _ensure_mongo_imports()
        return MongoUserRepository()
    return MemoryUserRepository()


def get_domain_repository() -> DomainRepository:
    """Get domain repository implementation based on configuration"""
    settings = get_settings()
    if settings.USE_MONGODB:
        _ensure_mongo_imports()
        return MongoDomainRepository()
    return MemoryDomainRepository()


def get_category_repository() -> CategoryRepository:
    """Get category repository implementation based on configuration"""
    settings = get_settings()
    if settings.USE_MONGODB:
        _ensure_mongo_imports()
        return MongoCategoryRepository()
    return MemoryCategoryRepository()


def get_asset_repository() -> AssetRepository:
    """Get asset repository implementation based on configuration"""
    settings = get_settings()
    if settings.USE_MONGODB:
        _ensure_mongo_imports()
        return MongoAssetRepository()
    return MemoryAssetRepository()


# Infrastructure persistence exports
__all__ = [
    "get_user_repository",
    "get_domain_repository",
    "get_category_repository",
    "get_asset_repository",
]
