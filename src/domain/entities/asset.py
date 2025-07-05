from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime, timezone
from ..enums.asset_type import AssetType


@dataclass
class Asset:
    name: str
    domain_id: UUID
    asset_type: AssetType
    content: str | None = None
    category_id: UUID | None = None
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
        """Check if the asset is soft deleted"""
        return self.deleted_at is not None

    def soft_delete(self):
        """Mark the asset as deleted"""
        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore a soft deleted asset"""
        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)

    def update(self):
        """Update the timestamp when asset is modified"""
        self.updated_at = datetime.now(timezone.utc)
