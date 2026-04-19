"""
RULE 3 — % gain/loss per BUY vs last close (split-adjusted entry). **No .pkl write.**

Exports (≤13 chars): `entry_gl_tb`
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

from . import entries


def entry_gl_tb(
    hist_display: pd.DataFrame,
    df_px: pd.DataFrame,
    stock_hist: dict[str, list[dict]] | None = None,
) -> pd.DataFrame:
    """
    Loops every ticker in `stock_hist` (default `MY_STOCKS`). Skips tickers with no BUY rows
    or missing price column — returns empty df if nothing to show (no crash).
    """
    if stock_hist is None:
        stock_hist = entries.MY_STOCKS
    if not stock_hist:
        return pd.DataFrame()

    tracking_rows: list[dict] = []
    for ticker in sorted(stock_hist.keys()):
        if hist_display is None or hist_display.empty or "ticker" not in hist_display.columns:
            continue
        sub = hist_display.loc[hist_display["ticker"] == ticker].reset_index(drop=True)
        buys = sub[sub["action"].str.startswith("BUY", na=False)]
        if buys.empty:
            continue

        if isinstance(df_px.columns, pd.MultiIndex) and (ticker, "Close") in df_px.columns:
            cl = df_px[ticker]["Close"].dropna()
            if cl.empty:
                continue
            last_close = float(cl.iloc[-1])
            date_range = df_px.index
        elif not isinstance(df_px.columns, pd.MultiIndex) and "Close" in df_px.columns:
            cl = df_px["Close"].dropna()
            if cl.empty:
                continue
            last_close = float(cl.iloc[-1])
            date_range = df_px.index
        else:
            continue

        history: Sequence[dict] = stock_hist.get(ticker, [])
        split_events: list[tuple[pd.Timestamp, float]] = []
        for e in history:
            if e.get("type") != "split":
                continue
            split_date = pd.to_datetime(e["date"])
            desc = str(e.get("description", ""))
            ratio = None
            if ":" in desc:
                parts = desc.split(":")
                try:
                    left = float(parts[0].strip().split()[-1])
                    right = float(parts[1].split()[0])
                    ratio = left / right
                except Exception:
                    ratio = None
            elif "-for-" in desc:
                parts = desc.split("-for-")
                try:
                    left = float(parts[0].strip().split()[-1])
                    right = float(parts[1].split()[0])
                    ratio = right / left
                except Exception:
                    ratio = None
            if ratio is not None:
                split_events.append((split_date, ratio))

        for _, buy_row in buys.iterrows():
            entry_date = pd.to_datetime(buy_row["date"])
            try:
                entry_price = float(str(buy_row["action"]).split("@")[-1])
            except Exception:
                entry_price = np.nan
            adj_entry_price = entry_price
            for split_date, ratio in split_events:
                if entry_date < split_date <= date_range[-1]:
                    adj_entry_price /= ratio
            pct_change = np.nan
            if not np.isnan(adj_entry_price) and not np.isnan(last_close):
                pct_change = 100.0 * (last_close - adj_entry_price) / adj_entry_price
            tracking_rows.append(
                {
                    "ticker": ticker,
                    "entry_date": entry_date.date(),
                    "adj_entry_price": adj_entry_price,
                    "last_close": last_close,
                    "pct_change": pct_change,
                }
            )

    return pd.DataFrame(tracking_rows)
