"""Small controlled evaluation set for the sample financial document."""

from __future__ import annotations

from app.schemas.models import EvaluationCase


EVALUATION_CASES = [
    EvaluationCase(
        case_id="growth-drivers",
        question="What drives ACME revenue growth?",
        expected_answer_points=["cloud software subscriptions", "enterprise customer expansion"],
        tags=["growth", "business-model"],
    ),
    EvaluationCase(
        case_id="business-quality",
        question="What business quality signals are mentioned for ACME?",
        expected_answer_points=["recurring revenue", "high renewal rates", "operating leverage"],
        tags=["business-model"],
    ),
    EvaluationCase(
        case_id="risk-factors",
        question="What are ACME's main risk factors?",
        expected_answer_points=["competition", "customer concentration", "sales cycle uncertainty", "margin pressure"],
        tags=["risk", "hallucination-control"],
    ),
    EvaluationCase(
        case_id="cost-pressure",
        question="What could pressure ACME margins?",
        expected_answer_points=["infrastructure costs", "margin pressure"],
        tags=["financial-performance", "risk"],
    ),
    EvaluationCase(
        case_id="unknown-dividend-policy",
        question="What is ACME's dividend policy?",
        expected_answer_points=["could not find", "relevant evidence", "current document library"],
        tags=["hallucination-control", "unknown-answer"],
    ),
]
