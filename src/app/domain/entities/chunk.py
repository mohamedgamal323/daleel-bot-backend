from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Chunk:
    asset_id: UUID
    text: str
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
