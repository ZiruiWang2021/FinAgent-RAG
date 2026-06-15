"""RAG question-answering API."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.schemas.models import AskRequest, AskResponse


router = APIRouter(tags=["rag"])


@router.post("/ask", response_model=AskResponse)
def ask(request: Request, payload: AskRequest) -> AskResponse:
    return request.app.state.container.rag_service.answer(
        question=payload.question,
        top_k=payload.top_k,
    )
