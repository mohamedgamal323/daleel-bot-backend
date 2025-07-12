from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime


@dataclass
class CreateCategoryRequestDto:
    """DTO for creating a new category"""
    name: str
    domain_id: UUID


@dataclass
class UpdateCategoryRequestDto:
    """DTO for updating an existing category"""
    name: Optional[str] = None
    domain_id: Optional[UUID] = None


@dataclass
class CategoryResponseDto:
    """DTO for category response"""
    id: UUID
    name: str
    domain_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
