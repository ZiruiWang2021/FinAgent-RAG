"""Report Agent."""

from __future__ import annotations

from app.schemas.models import RetrievedChunk, StockMetrics


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
