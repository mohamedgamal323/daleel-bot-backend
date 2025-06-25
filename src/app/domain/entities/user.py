from dataclasses import dataclass
from uuid import UUID, uuid4
from ..enums.role import Role


@dataclass
class User:
    username: str
    role: Role
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
