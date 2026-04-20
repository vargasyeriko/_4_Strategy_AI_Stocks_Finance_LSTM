"""
User input for `src_3` — growth vs defensive buckets and data locations.

Panel: MultiIndex OHLCV (Yahoo-style), default file resolved via `_0_paths.default_panel_path`.
"""
from __future__ import annotations

PANEL_FILENAME: str = "your_data.pkl"

NOISE_TICKERS: frozenset[str] = frozenset({"CURSOR", "OPEN", "LOVABLE"})

TICKER_ALIASES: dict[str, str] = {
    "APPL": "AAPL",
}

GROWTH_TICKERS: list[str] = [
    "NVDA",
    "AMD",
    "TSLA",
    "ROKU",
    "NFLX",
    "SOXX",
    "CRSP",
    "COIN",
    "HOOD",
    "PLTR",
    "ACHR",
    "SHOP",
    "RBLX",
]

DEFENSIVE_TICKERS: list[str] = [
    "AAPL",
    "TSM",
    "SSNLF",
    "ASML",
    "AVGO",
    "SOBO",
    "TREE",
    "ANDE",
]

TARGET_WEIGHT_GROWTH: float = 0.58
TARGET_WEIGHT_DEFENSIVE: float = 0.42
