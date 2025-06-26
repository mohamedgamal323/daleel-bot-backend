from typing import Iterable, Tuple
from ..interfaces.llm_provider import LLMProvider
from ..interfaces.vector_db import VectorDB
from ...domain.entities.asset import Asset


class QueryService:
    def __init__(self, llm: LLMProvider, vector_db: VectorDB):
        self._llm = llm
        self._vector_db = vector_db

    def query(self, domain_id, text: str) -> Tuple[str, Iterable[Asset]]:
        embedding = self._llm.embed(text)
        assets = self._vector_db.search(domain_id, embedding)
        answer = self._llm.complete(text)
        return answer, assets
