"""Main dependency injection module - orchestrates all layers"""

from src.application.services.user_service import UserService
from src.application.services.asset_service import AssetService
from src.application.services.domain_service import DomainService
from src.application.services.category_service import CategoryService
from src.infrastructure_persistence.dependencies import (
    get_user_repository,
    get_asset_repository,
    get_domain_repository,
    get_category_repository,
)
from src.infrastructure_integration.dependencies import (
    get_llm_provider,
    get_vector_db,
)
from .config import get_settings


def get_user_service() -> UserService:
    """Get user service with appropriate repository"""
    repo = get_user_repository()
    return UserService(repo)


def get_domain_service() -> DomainService:
    """Get domain service with appropriate repository"""
    repo = get_domain_repository()
    return DomainService(repo)


def get_category_service() -> CategoryService:
    """Get category service with appropriate repository"""
    repo = get_category_repository()
    return CategoryService(repo)


def get_asset_service() -> AssetService:
    """Get asset service with appropriate repository and integrations"""
    settings = get_settings()
    repo = get_asset_repository()
    llm_provider = get_llm_provider(settings.LLM_PROVIDER)
    vector_db = get_vector_db(settings.VECTOR_DB, repo)
    return AssetService(repo, llm_provider, vector_db)
