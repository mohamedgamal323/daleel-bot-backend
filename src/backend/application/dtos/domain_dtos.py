from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from datetime import datetime


@dataclass
class CreateDomainRequestDto:
    """DTO for creating a new domain"""
    name: str


@dataclass
class UpdateDomainRequestDto:
    """DTO for updating an existing domain"""
    name: Optional[str] = None


@dataclass
class DomainResponseDto:
    """DTO for domain response"""
    id: UUID
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
