"""Document index inspection API."""

from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Request

from app.schemas.models import DocumentSummary, DocumentsResponse


router = APIRouter(tags=["documents"])


@router.get("/documents", response_model=DocumentsResponse)
def list_documents(request: Request) -> DocumentsResponse:
    chunks = request.app.state.container.vector_store.chunks
    counts = Counter(chunk.source for chunk in chunks)
    return DocumentsResponse(
        total_chunks=len(chunks),
        documents=[
            DocumentSummary(source=source, chunks=count)
            for source, count in sorted(counts.items())
        ],
    )
