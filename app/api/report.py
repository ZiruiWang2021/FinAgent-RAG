"""Multi-agent report API."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.schemas.models import ReportRequest, ReportResponse


router = APIRouter(tags=["agents"])


@router.post("/generate-report", response_model=ReportResponse)
def generate_report(request: Request, payload: ReportRequest) -> ReportResponse:
    return request.app.state.container.workflow.run(
        question=payload.question,
        ticker=payload.ticker,
        top_k=payload.top_k,
    )
