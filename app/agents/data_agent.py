"""Data Agent."""

from __future__ import annotations

from app.schemas.models import StockMetrics
from app.tools.stock_data_tool import StockDataTool


class DataAgent:
    name = "Data Agent"

    def __init__(self, stock_tool: StockDataTool):
        self.stock_tool = stock_tool

    def run(self, ticker: str, period: str = "6mo") -> StockMetrics:
        return self.stock_tool.analyze(ticker=ticker, period=period).metrics
