from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime, timezone
from ..enums.role import Role


@dataclass
class User:
    username: str
    role: Role
    password_hash: str | None = None  # Stores hashed password
    email: str | None = None  # Optional email field
    is_active: bool = True  # Account active status
    last_login: datetime | None = None  # Track last login
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)

    def is_deleted(self) -> bool:
        """Check if the user is soft deleted"""
        return self.deleted_at is not None

    def soft_delete(self):
        """Mark the user as deleted"""
        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore a soft deleted user"""
        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)

    def update(self):
        """Update the timestamp when user is modified"""
        self.updated_at = datetime.now(timezone.utc)

    def set_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now(timezone.utc)
        self.update()
