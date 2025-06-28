from dataclasses import dataclass
from uuid import UUID, uuid4
from ..enums.asset_type import AssetType


@dataclass
class Asset:
    name: str
    domain_id: UUID
    asset_type: AssetType
    content: str | None = None
    category_id: UUID | None = None
    id: UUID | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
