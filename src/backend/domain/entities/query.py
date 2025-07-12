from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Query:
    user_id: UUID
    text: str
    domain_id: UUID
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
