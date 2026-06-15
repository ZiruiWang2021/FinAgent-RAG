"""Chunk financial documents into retrieval-friendly passages."""

from __future__ import annotations

from pathlib import Path

from app.rag.document_loader import normalize_text
from app.schemas.models import SourceChunk


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[SourceChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0:
        raise ValueError("overlap cannot be negative.")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    normalized = normalize_text(text)
    if not normalized:
        return []

    chunks: list[SourceChunk] = []
    start = 0
    index = 0

    while start < len(normalized):
        hard_end = min(start + chunk_size, len(normalized))
        end = _prefer_sentence_boundary(normalized, start, hard_end, chunk_size)
        content = normalized[start:end].strip()

        if content:
            chunks.append(
                SourceChunk(
                    chunk_id=f"{Path(source).name}#{index}",
                    source=source,
                    content=content,
                    char_start=start,
                    char_end=end,
                    metadata={"chunk_index": index},
                )
            )
            index += 1

        if end >= len(normalized):
            break

        start = max(0, end - overlap)
        if chunks and start <= chunks[-1].char_start:
            start = end

    return chunks


def _prefer_sentence_boundary(text: str, start: int, hard_end: int, chunk_size: int) -> int:
    if hard_end >= len(text):
        return hard_end

    min_reasonable_end = start + int(chunk_size * 0.6)
    boundary_chars = [".", "!", "?", "\n", ";", "。", "！", "？", "；"]
    best = max(text.rfind(char, start, hard_end) for char in boundary_chars)
    if best >= min_reasonable_end:
        return best + 1

    whitespace = text.rfind(" ", start, hard_end)
    if whitespace >= min_reasonable_end:
        return whitespace

    return hard_end
