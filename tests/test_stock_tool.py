import pandas as pd

from app.tools.financial_metrics import calculate_stock_metrics


def test_calculate_stock_metrics_for_uptrend():
    dates = pd.date_range("2024-01-01", periods=80, freq="B")
    close = [100 + index for index in range(80)]
    history = pd.DataFrame({"Close": close}, index=dates)

    metrics = calculate_stock_metrics(history, ticker="TEST")

    assert metrics.ticker == "TEST"
    assert metrics.latest_close == 179
    assert metrics.one_month_return_pct > 0
    assert metrics.annualized_volatility_pct >= 0
    assert metrics.ma20 > metrics.ma60
    assert metrics.max_drawdown_pct == 0
    assert metrics.trend.startswith("Bullish")


def test_calculate_stock_metrics_for_drawdown():
    dates = pd.date_range("2024-01-01", periods=5, freq="B")
    history = pd.DataFrame({"Close": [100, 120, 90, 95, 80]}, index=dates)

    metrics = calculate_stock_metrics(history, ticker="DROP")

    assert metrics.max_drawdown_pct == -33.33
    assert metrics.latest_close == 80
