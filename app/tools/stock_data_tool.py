"""Tool for fetching stock data and returning calculated metrics."""

from __future__ import annotations

import pandas as pd

from app.schemas.models import StockAnalysisResponse
from app.tools.financial_metrics import calculate_stock_metrics

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    yf = None


class StockDataTool:
    def fetch_history(self, ticker: str, period: str = "6mo") -> pd.DataFrame:
        if yf is None:
            raise RuntimeError("yfinance is not installed. Install requirements.txt first.")

        history = yf.download(
            ticker,
            period=period,
            auto_adjust=True,
            progress=False,
            group_by="column",
        )
        if history.empty:
            raise ValueError(f"No market data returned for ticker '{ticker}'.")
        return history

    def analyze(self, ticker: str, period: str = "6mo") -> StockAnalysisResponse:
        normalized_ticker = ticker.upper()
        history = self.fetch_history(normalized_ticker, period=period)
        metrics = calculate_stock_metrics(history, normalized_ticker)
        return StockAnalysisResponse(metrics=metrics, rows=len(history))
