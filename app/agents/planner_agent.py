"""Planner Agent."""

from __future__ import annotations


class PlannerAgent:
    name = "Planner Agent"

    def run(self, question: str, ticker: str | None = None) -> list[str]:
        steps = [
            "Clarify the financial analysis objective.",
            "Retrieve relevant source evidence from uploaded documents.",
        ]
        if ticker:
            steps.append(f"Call the stock data tool for ticker {ticker.upper()}.")
        steps.extend(
            [
                "Summarize business, market, financial, and regulatory risks.",
                "Generate a structured report with citations and tool outputs.",
            ]
        )
        return steps
