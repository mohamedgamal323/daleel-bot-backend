import pytest
from src.application.services.domain_service import DomainService
from src.infrastructure_persistence.memory_domain_repo import MemoryDomainRepository


@pytest.mark.asyncio
async def test_create_and_list_domain():
    repo = MemoryDomainRepository()
    # For testing, we can instantiate directly with the repository
    service = DomainService(repo)
    await service.create_domain("education")
    domains = await service.list_domains()
    assert len(domains) == 1
    assert domains[0].name == "education"
from src.application.services.domain_service import DomainService
from src.infrastructure_persistence.memory_domain_repo import MemoryDomainRepository


@pytest.mark.asyncio
async def test_create_and_list_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    await service.create_domain("HR")
    domains = await service.list_domains()
    assert len(domains) == 1
    assert domains[0].name == "HR"
