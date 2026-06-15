"""Stock analysis API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.schemas.models import StockAnalysisRequest, StockAnalysisResponse


router = APIRouter(tags=["stock"])


@router.post("/analyze-stock", response_model=StockAnalysisResponse)
def analyze_stock(request: Request, payload: StockAnalysisRequest) -> StockAnalysisResponse:
    try:
        return request.app.state.container.stock_tool.analyze(
            ticker=payload.ticker,
            period=payload.period,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
