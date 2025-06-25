from src.app.application.services.domain_service import DomainService
from src.app.infrastructure.repositories.memory_domain_repo import MemoryDomainRepository


def test_create_and_list_domain():
    repo = MemoryDomainRepository()
    service = DomainService(repo)
    service.create_domain("HR")
    domains = list(service.list_domains())
    assert len(domains) == 1
    assert domains[0].name == "HR"
