from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class AuditLog:
    user_id: UUID
    action: str
    timestamp: datetime | None = None
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
