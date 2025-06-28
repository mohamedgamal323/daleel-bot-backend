from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Category:
    name: str
    domain_id: UUID
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
