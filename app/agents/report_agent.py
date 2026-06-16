"""Report Agent."""

from __future__ import annotations

from app.schemas.models import Citation, RetrievedChunk, RiskItem, StockMetrics, StructuredReport


class ReportAgent:
    name = "Report Agent"

    def run(
        self,
        question: str,
        sources: list[RetrievedChunk],
        risks: str,
        stock_analysis: StockMetrics | None = None,
    ) -> str:
        return f"""# FinAgent-RAG Analysis Report

## Executive Summary
The analysis addresses: {question}

The document view is grounded in retrieved source passages. The market-data view is included when a ticker is provided.

## Retrieved Evidence
{self._format_evidence(sources)}

## Stock Data Analysis
{self._format_stock(stock_analysis)}

## Key Risks
{risks}

## Analyst Takeaway
Use the cited evidence as a starting point for deeper diligence. For production, connect this workflow to a stronger LLM, persistent vector storage, scheduled data refreshes, and formal evaluation sets.
"""

    def build_structured_report(
        self,
        question: str,
        sources: list[RetrievedChunk],
        risks: str,
        stock_analysis: StockMetrics | None = None,
    ) -> StructuredReport:
        citations = [
            Citation(
                source=source.source,
                chunk_id=source.chunk_id,
                score=source.score,
                quote=source.content[:240].strip(),
            )
            for source in sources
        ]
        risk_items = self._build_risk_items(risks)
        key_findings = self._build_key_findings(sources=sources, stock_analysis=stock_analysis)

        return StructuredReport(
            title="FinAgent-RAG Structured Financial Analysis",
            executive_summary=(
                "This report combines retrieved document evidence with optional stock market metrics. "
                "Claims from uploaded documents are tied to citations to reduce hallucination risk."
            ),
            key_findings=key_findings,
            risks=risk_items,
            citations=citations,
            stock_metrics=stock_analysis,
            hallucination_controls=[
                "Answers are generated from retrieved chunks only when sources are available.",
                "Each document-grounded finding keeps source, chunk id, and retrieval score.",
                "The evaluation module checks expected answer points and source coverage.",
                "The report separates retrieved evidence from stock-data tool output.",
            ],
        )

    def _format_evidence(self, sources: list[RetrievedChunk]) -> str:
        if not sources:
            return "No relevant document evidence was retrieved."

        lines = []
        for source in sources:
            snippet = source.content[:280].strip()
            if len(source.content) > 280:
                snippet += "..."
            lines.append(f"- {snippet} `[source: {source.source}, score: {source.score:.2f}]`")
        return "\n".join(lines)

    def _format_stock(self, stock_analysis: StockMetrics | None) -> str:
        if stock_analysis is None:
            return "No ticker was provided, so market-data analysis was skipped."

        return (
            f"- Ticker: {stock_analysis.ticker}\n"
            f"- Date range: {stock_analysis.start_date} to {stock_analysis.end_date}\n"
            f"- Latest close: {stock_analysis.latest_close}\n"
            f"- 1-month return: {stock_analysis.one_month_return_pct}%\n"
            f"- Annualized volatility: {stock_analysis.annualized_volatility_pct}%\n"
            f"- 20-day moving average: {stock_analysis.ma20}\n"
            f"- 60-day moving average: {stock_analysis.ma60}\n"
            f"- Maximum drawdown: {stock_analysis.max_drawdown_pct}%\n"
            f"- Trend: {stock_analysis.trend}"
        )

    def _build_key_findings(
        self,
        sources: list[RetrievedChunk],
        stock_analysis: StockMetrics | None,
    ) -> list[str]:
        findings = []
        for source in sources[:3]:
            snippet = source.content[:180].strip()
            if len(source.content) > 180:
                snippet += "..."
            findings.append(f"Document evidence from {source.source}: {snippet}")

        if stock_analysis is not None:
            findings.append(
                f"{stock_analysis.ticker} market signal: {stock_analysis.one_month_return_pct}% 1-month return, "
                f"{stock_analysis.annualized_volatility_pct}% annualized volatility, {stock_analysis.trend}."
            )
        return findings

    def _build_risk_items(self, risks: str) -> list[RiskItem]:
        if not risks or risks.startswith("No risk evidence"):
            return [
                RiskItem(
                    name="Insufficient retrieved risk evidence",
                    severity="unknown",
                    evidence=risks or "No risk evidence available.",
                )
            ]

        items = []
        for line in risks.splitlines():
            evidence = line.lstrip("- ").strip()
            if evidence:
                items.append(
                    RiskItem(
                        name="Retrieved risk factor",
                        severity="medium",
                        evidence=evidence,
                    )
                )
        return items
