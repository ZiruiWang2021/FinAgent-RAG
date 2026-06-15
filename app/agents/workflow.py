"""Agent workflow orchestration."""

from __future__ import annotations

from app.agents.data_agent import DataAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.report_agent import ReportAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.risk_agent import RiskAgent
from app.rag.retriever import RagService
from app.schemas.models import ReportResponse, StockMetrics, WorkflowStep
from app.tools.stock_data_tool import StockDataTool


class AgentWorkflow:
    def __init__(self, rag_service: RagService, stock_tool: StockDataTool):
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent(rag_service)
        self.data = DataAgent(stock_tool)
        self.risk = RiskAgent()
        self.report = ReportAgent()

    def run(self, question: str, ticker: str | None = None, top_k: int = 4) -> ReportResponse:
        steps: list[WorkflowStep] = []

        plan = self.planner.run(question=question, ticker=ticker)
        steps.append(
            WorkflowStep(
                agent=self.planner.name,
                action="Create analysis plan",
                output="\n".join(f"{index + 1}. {step}" for index, step in enumerate(plan)),
            )
        )

        sources = self.retriever.run(question=question, top_k=top_k)
        steps.append(
            WorkflowStep(
                agent=self.retriever.name,
                action="Retrieve document evidence",
                output=f"Retrieved {len(sources)} relevant chunks.",
            )
        )

        stock_analysis: StockMetrics | None = None
        if ticker:
            try:
                stock_analysis = self.data.run(ticker=ticker)
                data_output = (
                    f"{stock_analysis.ticker}: {stock_analysis.one_month_return_pct}% 1-month return, "
                    f"{stock_analysis.annualized_volatility_pct}% annualized volatility, "
                    f"{stock_analysis.trend}."
                )
            except Exception as exc:  # pragma: no cover
                data_output = f"Stock analysis failed: {exc}"

            steps.append(
                WorkflowStep(
                    agent=self.data.name,
                    action="Analyze ticker market data",
                    output=data_output,
                )
            )

        risks = self.risk.run(sources)
        steps.append(WorkflowStep(agent=self.risk.name, action="Summarize risk factors", output=risks))

        report = self.report.run(question=question, sources=sources, risks=risks, stock_analysis=stock_analysis)
        steps.append(WorkflowStep(agent=self.report.name, action="Generate structured report", output="Report generated."))

        return ReportResponse(
            question=question,
            ticker=ticker.upper() if ticker else None,
            steps=steps,
            report=report,
            sources=sources,
            stock_analysis=stock_analysis,
        )
