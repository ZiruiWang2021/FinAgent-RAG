"""In-memory vector store with cosine similarity search."""

from __future__ import annotations

import numpy as np

from app.rag.embeddings import HashingEmbeddingModel
from app.schemas.models import RetrievedChunk, SourceChunk


class InMemoryVectorStore:
    def __init__(self, embedding_model: HashingEmbeddingModel | None = None):
        self.embedding_model = embedding_model or HashingEmbeddingModel()
        self._chunks: list[SourceChunk] = []
        self._vectors: np.ndarray | None = None

    def __len__(self) -> int:
        return len(self._chunks)

    @property
    def chunks(self) -> list[SourceChunk]:
        return list(self._chunks)

    def clear(self) -> None:
        self._chunks = []
        self._vectors = None

    def add_chunks(self, chunks: list[SourceChunk]) -> None:
        if not chunks:
            return

        new_vectors = np.vstack([self.embedding_model.embed(chunk.content) for chunk in chunks])
        self._vectors = new_vectors if self._vectors is None else np.vstack([self._vectors, new_vectors])
        self._chunks.extend(chunks)

    def search(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        if not self._chunks or self._vectors is None:
            return []

        query_vector = self.embedding_model.embed(query)
        if not np.any(query_vector):
            return []

        scores = self._vectors @ query_vector
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        results: list[RetrievedChunk] = []
        for index in ranked_indices:
            score = float(scores[index])
            if score <= 0:
                continue
            chunk = self._chunks[int(index)]
            results.append(RetrievedChunk(**chunk.model_dump(), score=round(score, 4)))
        return results
