from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class Permissions:
    domain_ids: List[UUID]
