"""Pydantic models for the API, RAG pipeline, tools, and agents."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SourceChunk(BaseModel):
    chunk_id: str
    source: str
    content: str
    char_start: int = 0
    char_end: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(SourceChunk):
    score: float = 0.0


class UploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(4, ge=1, le=10)


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[RetrievedChunk] = Field(default_factory=list)


class StockAnalysisRequest(BaseModel):
    ticker: str = Field(..., min_length=1, examples=["AAPL"])
    period: str = Field("6mo", examples=["6mo", "1y", "2y"])


class StockMetrics(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    latest_close: float
    one_month_return_pct: float
    annualized_volatility_pct: float
    ma20: float
    ma60: float
    max_drawdown_pct: float
    trend: str


class StockAnalysisResponse(BaseModel):
    metrics: StockMetrics
    rows: int


class WorkflowStep(BaseModel):
    agent: str
    action: str
    output: str


class ReportRequest(BaseModel):
    question: str = Field(..., min_length=1)
    ticker: str | None = Field(None, examples=["MSFT"])
    top_k: int = Field(4, ge=1, le=10)


class ReportResponse(BaseModel):
    question: str
    ticker: str | None = None
    steps: list[WorkflowStep]
    report: str
    sources: list[RetrievedChunk] = Field(default_factory=list)
    stock_analysis: StockMetrics | None = None
