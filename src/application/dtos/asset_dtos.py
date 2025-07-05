from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime
from src.domain.enums.asset_type import AssetType


@dataclass
class CreateAssetRequestDto:
    """DTO for creating a new asset"""
    name: str
    domain_id: UUID
    asset_type: AssetType
    content: Optional[str] = None
    category_id: Optional[UUID] = None


@dataclass
class UpdateAssetRequestDto:
    """DTO for updating an existing asset"""
    name: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[UUID] = None


@dataclass
class AssetResponseDto:
    """DTO for asset response"""
    id: UUID
    name: str
    domain_id: UUID
    asset_type: AssetType
    content: Optional[str] = None
    category_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
