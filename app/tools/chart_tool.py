"""Chart-ready data helpers for the Streamlit demo."""

from __future__ import annotations

import pandas as pd

from app.tools.financial_metrics import extract_close_series


def build_price_chart_rows(history: pd.DataFrame) -> list[dict[str, str | float]]:
    close = extract_close_series(history)
    ma20 = close.rolling(window=20, min_periods=1).mean()
    ma60 = close.rolling(window=60, min_periods=1).mean()

    rows = []
    for date, price in close.items():
        rows.append(
            {
                "date": date.date().isoformat() if hasattr(date, "date") else str(date),
                "close": round(float(price), 4),
                "ma20": round(float(ma20.loc[date]), 4),
                "ma60": round(float(ma60.loc[date]), 4),
            }
        )
    return rows
