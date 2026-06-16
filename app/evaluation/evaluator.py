"""Simple evaluation logic for source-grounded RAG answers."""

from __future__ import annotations

from app.rag.retriever import RagService
from app.schemas.models import EvaluationCase, EvaluationResponse, EvaluationResult


def evaluate_rag_cases(
    rag_service: RagService,
    cases: list[EvaluationCase],
    top_k: int = 4,
) -> EvaluationResponse:
    results = [_evaluate_case(rag_service=rag_service, case=case, top_k=top_k) for case in cases]
    passed_cases = sum(result.passed for result in results)
    average_score = round(
        sum(result.groundedness_score for result in results) / len(results),
        3,
    ) if results else 0.0
    return EvaluationResponse(
        total_cases=len(results),
        passed_cases=passed_cases,
        average_groundedness_score=average_score,
        results=results,
    )


def _evaluate_case(rag_service: RagService, case: EvaluationCase, top_k: int) -> EvaluationResult:
    response = rag_service.answer(case.question, top_k=top_k)
    haystack = f"{response.answer}\n" + "\n".join(source.content for source in response.sources)
    haystack = haystack.lower()

    matched_points = [
        point for point in case.expected_answer_points
        if point.lower() in haystack
    ]
    missing_points = [
        point for point in case.expected_answer_points
        if point not in matched_points
    ]
    point_score = len(matched_points) / len(case.expected_answer_points) if case.expected_answer_points else 0.0
    source_score = 1.0 if response.sources or "unknown-answer" in case.tags else 0.0
    groundedness_score = round((point_score * 0.7) + (source_score * 0.3), 3)

    return EvaluationResult(
        case_id=case.case_id,
        question=case.question,
        expected_answer_points=case.expected_answer_points,
        matched_points=matched_points,
        missing_points=missing_points,
        source_count=len(response.sources),
        groundedness_score=groundedness_score,
        passed=groundedness_score >= 0.65,
        answer_preview=response.answer[:500],
    )
