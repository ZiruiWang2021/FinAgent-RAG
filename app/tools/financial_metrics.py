"""Financial market metric calculations."""

from __future__ import annotations

import math

import pandas as pd

from app.schemas.models import StockMetrics


def calculate_stock_metrics(history: pd.DataFrame, ticker: str) -> StockMetrics:
    close = extract_close_series(history)
    if close.empty:
        raise ValueError("History must include non-empty Close prices.")

    latest_close = float(close.iloc[-1])
    lookback_index = -22 if len(close) >= 22 else 0
    one_month_return = latest_close / float(close.iloc[lookback_index]) - 1

    daily_returns = close.pct_change().dropna()
    annualized_volatility = float(daily_returns.std() * math.sqrt(252)) if not daily_returns.empty else 0.0

    ma20 = float(close.rolling(window=20, min_periods=1).mean().iloc[-1])
    ma60 = float(close.rolling(window=60, min_periods=1).mean().iloc[-1])

    running_peak = close.cummax()
    max_drawdown = float((close / running_peak - 1).min())

    return StockMetrics(
        ticker=ticker.upper(),
        start_date=_date_to_str(close.index[0]),
        end_date=_date_to_str(close.index[-1]),
        latest_close=round(latest_close, 4),
        one_month_return_pct=round(one_month_return * 100, 2),
        annualized_volatility_pct=round(annualized_volatility * 100, 2),
        ma20=round(ma20, 4),
        ma60=round(ma60, 4),
        max_drawdown_pct=round(max_drawdown * 100, 2),
        trend=infer_trend(latest_close=latest_close, ma20=ma20, ma60=ma60),
    )


def infer_trend(latest_close: float, ma20: float, ma60: float) -> str:
    if latest_close > ma20 > ma60:
        return "Bullish: price is above both moving averages"
    if latest_close < ma20 < ma60:
        return "Bearish: price is below both moving averages"
    return "Mixed: moving averages do not confirm a clear trend"


def extract_close_series(history: pd.DataFrame) -> pd.Series:
    if isinstance(history.columns, pd.MultiIndex):
        close = history.xs("Close", axis=1, level=0, drop_level=False)
        series = close.iloc[:, 0]
    elif "Close" in history.columns:
        series = history["Close"]
    elif "Adj Close" in history.columns:
        series = history["Adj Close"]
    else:
        raise ValueError("History must contain a Close or Adj Close column.")

    return pd.to_numeric(series, errors="coerce").dropna()


def _date_to_str(value) -> str:
    if hasattr(value, "date"):
        return value.date().isoformat()
    return str(value)
