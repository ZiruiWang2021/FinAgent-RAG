"""Document upload API."""

from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.schemas.models import UploadResponse


router = APIRouter(tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload(request: Request, file: UploadFile = File(...)) -> UploadResponse:
    try:
        content = await file.read()
        chunks = request.app.state.container.document_indexer.add_document(
            file.filename or "uploaded.txt",
            content,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process upload: {exc}") from exc

    return UploadResponse(
        filename=file.filename or "uploaded.txt",
        chunks_indexed=len(chunks),
        message="Document uploaded, chunked, embedded, and indexed.",
    )
