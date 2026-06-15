"""Document indexing, retrieval, and RAG answer synthesis."""

from __future__ import annotations

import re
from pathlib import Path

from app.rag.chunker import chunk_text
from app.rag.document_loader import extract_text_from_bytes
from app.rag.vector_store import InMemoryVectorStore
from app.schemas.models import AskResponse, RetrievedChunk, SourceChunk


class DocumentIndexer:
    def __init__(self, vector_store: InMemoryVectorStore, chunk_size: int = 800, chunk_overlap: int = 120):
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def add_document(self, filename: str, content: bytes) -> list[SourceChunk]:
        text = extract_text_from_bytes(filename, content)
        chunks = chunk_text(
            text=text,
            source=Path(filename).name,
            chunk_size=self.chunk_size,
            overlap=self.chunk_overlap,
        )
        self.vector_store.add_chunks(chunks)
        return chunks


class RagRetriever:
    def __init__(self, vector_store: InMemoryVectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        return self.vector_store.search(query, top_k=top_k)


class RagService:
    def __init__(self, retriever: RagRetriever):
        self.retriever = retriever

    @property
    def vector_store(self) -> InMemoryVectorStore:
        return self.retriever.vector_store

    def answer(self, question: str, top_k: int = 4) -> AskResponse:
        sources = self.retriever.retrieve(question, top_k=top_k)
        answer = self._synthesize_answer(question, sources)
        return AskResponse(question=question, answer=answer, sources=sources)

    def _synthesize_answer(self, question: str, sources: list[RetrievedChunk]) -> str:
        if not sources:
            return (
                "I could not find relevant evidence in the current document library. "
                "Upload company reports, filings, or research notes, then ask again."
            )

        bullets = []
        for source in sources:
            snippet = _best_snippet(source.content, question)
            bullets.append(f"- {snippet} [source: {source.source}, score: {source.score:.2f}]")
        return "Based on the retrieved document evidence, the main points are:\n" + "\n".join(bullets)


def _best_snippet(content: str, question: str, max_chars: int = 360) -> str:
    sentences = re.split(r"(?<=[.!?。！？])\s+", content.strip())
    question_terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_\u4e00-\u9fff]+", question)}

    def score(sentence: str) -> int:
        terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_\u4e00-\u9fff]+", sentence)}
        return len(question_terms & terms)

    best = max(sentences, key=score) if sentences else content
    if len(best) <= max_chars:
        return best.strip()
    return best[: max_chars - 3].rstrip() + "..."
