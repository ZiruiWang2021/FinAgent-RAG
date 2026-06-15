"""Retriever Agent."""

from __future__ import annotations

from app.rag.retriever import RagService
from app.schemas.models import RetrievedChunk


class RetrieverAgent:
    name = "Retriever Agent"

    def __init__(self, rag_service: RagService):
        self.rag_service = rag_service

    def run(self, question: str, top_k: int = 4) -> list[RetrievedChunk]:
        return self.rag_service.retriever.retrieve(question, top_k=top_k)
