"""
RULE 3 — Final portfolio summary table (per ticker). **No .pkl write.**

Exports (≤13 chars): `portf_sum_tb`, `earn_summ_tb`
"""
from __future__ import annotations

import pandas as pd


def earn_summ_tb(per_ticker_df: pd.DataFrame) -> pd.DataFrame:
    """
    Portfolio-level summary from the per-ticker table (one row per metric).

    ``sum_ledger_net_cash_flow_usd`` is the sum of per-ticker cumulative ledger
    cash flows (buys negative, sells/dividends positive, etc.).

    ``mark_to_market_plus_ledger_cashflow_usd`` equals total open market value
    plus that sum; for positions fully captured in the ledger it matches the
    usual ``position_value + net_cash_flow`` picture per ticker, aggregated.
    """
    if per_ticker_df is None or per_ticker_df.empty:
        return pd.DataFrame(columns=["metric", "value"])
    df = per_ticker_df.copy()
    pos = pd.to_numeric(df.get("position_value_usd"), errors="coerce")
    cash = pd.to_numeric(df.get("net_cash_flow_usd"), errors="coerce")
    sh = pd.to_numeric(df.get("shares_now"), errors="coerce").fillna(0.0)
    total_pos = float(pos.sum(skipna=True))
    total_cash = float(cash.sum(skipna=True))
    mtm_plus = total_pos + total_cash
    n_ledger = int(len(df))
    n_held = int((sh > 1e-12).sum())
    out = pd.DataFrame(
        {
            "metric": [
                "total_market_value_stocks_usd",
                "sum_ledger_net_cash_flow_usd",
                "mark_to_market_plus_ledger_cashflow_usd",
                "tickers_in_ledger_count",
                "tickers_with_shares_now_count",
            ],
            "value": pd.Series([total_pos, total_cash, mtm_plus, n_ledger, n_held], dtype=object),
        }
    )
    return out


def portf_sum_tb(summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Last-stage portfolio table: shares, last close, value, net cash flow.
    Pass-through copy so callers can chain; empty in → empty out.
    """
    if summary_df is None or summary_df.empty:
        return pd.DataFrame()
    return summary_df.copy()
