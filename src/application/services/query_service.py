from typing import Iterable, Tuple
from fastapi import Depends
from ..integration.llm_provider import LLMProvider
from ..vectordb.vector_db import VectorDB
from src.domain.entities.asset import Asset
from ..integration.dependencies import get_llm_provider, get_vector_db


class QueryService:
    def __init__(
        self, 
        llm: LLMProvider = Depends(get_llm_provider),
        vector_db: VectorDB = Depends(get_vector_db)
    ):
        self._llm = llm
        self._vector_db = vector_db

    def query(self, domain_id, text: str) -> Tuple[str, Iterable[Asset]]:
        embedding = self._llm.embed(text)
        assets = self._vector_db.search(domain_id, embedding)
        answer = self._llm.complete(text)
        return answer, assets
