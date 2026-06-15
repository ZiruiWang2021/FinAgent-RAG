"""Risk Agent."""

from __future__ import annotations

import re

from app.schemas.models import RetrievedChunk


RISK_KEYWORDS = {
    "risk",
    "risks",
    "uncertainty",
    "debt",
    "leverage",
    "competition",
    "regulation",
    "regulatory",
    "decline",
    "margin",
    "liquidity",
    "litigation",
    "macroeconomic",
    "inflation",
    "supply",
    "impairment",
    "volatility",
    "风险",
    "竞争",
    "监管",
    "债务",
    "下滑",
}


class RiskAgent:
    name = "Risk Agent"

    def run(self, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "No risk evidence was retrieved from the current document library."

        risk_sentences: list[str] = []
        for chunk in chunks:
            for sentence in re.split(r"(?<=[.!?。！？])\s+", chunk.content):
                terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_\u4e00-\u9fff]+", sentence)}
                if terms & RISK_KEYWORDS:
                    risk_sentences.append(sentence.strip())

        unique = list(dict.fromkeys(sentence for sentence in risk_sentences if sentence))
        if not unique:
            return (
                "No explicit risk sentence was found in the retrieved passages. "
                "Review market, execution, competition, and balance-sheet exposure manually."
            )
        return "\n".join(f"- {sentence}" for sentence in unique[:5])
