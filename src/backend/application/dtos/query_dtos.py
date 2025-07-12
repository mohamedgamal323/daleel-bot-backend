from dataclasses import dataclass
from uuid import UUID
from typing import List


@dataclass 
class QueryRequestDto:
    """DTO for query request"""
    domain_id: UUID
    text: str


@dataclass
class AssetSummaryDto:
    """DTO for asset summary in query response"""
    id: UUID
    name: str


@dataclass
class QueryResponseDto:
    """DTO for query response"""
    answer: str
    assets: List[AssetSummaryDto]
