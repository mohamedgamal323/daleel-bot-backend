"""Application layer dependencies - business services and integration interfaces"""

from .services.user_service import UserService
from .services.domain_service import DomainService
from .services.category_service import CategoryService
from .services.asset_service import AssetService
from .services.auth_service import AuthService
from .services.query_service import QueryService

from .integration.llm_provider import LLMProvider
from .integration.vector_db import VectorDB

from ..domain.persistence.user_repository import UserRepository
from ..domain.persistence.domain_repository import DomainRepository
from ..domain.persistence.category_repository import CategoryRepository
from ..domain.persistence.asset_repository import AssetRepository


def get_user_service(user_repo: UserRepository) -> UserService:
    """Create user service with dependencies"""
    return UserService(user_repo)


def get_domain_service(domain_repo: DomainRepository) -> DomainService:
    """Create domain service with dependencies"""
    return DomainService(domain_repo)


def get_category_service(category_repo: CategoryRepository) -> CategoryService:
    """Create category service with dependencies"""
    return CategoryService(category_repo)


def get_asset_service(
    asset_repo: AssetRepository,
    llm_provider: LLMProvider | None = None,
    vector_db: VectorDB | None = None
) -> AssetService:
    """Create asset service with dependencies"""
    return AssetService(asset_repo, llm_provider, vector_db)


# Application layer exports
__all__ = [
    "UserService",
    "DomainService",
    "CategoryService", 
    "AssetService",
    "AuthService",
    "QueryService",
    "LLMProvider",
    "VectorDB",
    "UserRepository",
    "DomainRepository",
    "CategoryRepository",
    "AssetRepository",
    "get_user_service",
    "get_domain_service",
    "get_category_service",
    "get_asset_service",
]
