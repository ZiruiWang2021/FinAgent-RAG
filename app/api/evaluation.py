"""Evaluation API for retrieval quality and hallucination checks."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.evaluation.cases import EVALUATION_CASES
from app.evaluation.evaluator import evaluate_rag_cases
from app.schemas.models import EvaluationCase, EvaluationResponse


router = APIRouter(tags=["evaluation"])


@router.get("/evaluation-cases", response_model=list[EvaluationCase])
def get_evaluation_cases() -> list[EvaluationCase]:
    return EVALUATION_CASES


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: Request) -> EvaluationResponse:
    return evaluate_rag_cases(
        rag_service=request.app.state.container.rag_service,
        cases=EVALUATION_CASES,
        top_k=4,
    )
