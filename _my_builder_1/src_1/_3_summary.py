"""
RULE 3 — Final portfolio summary table (per ticker). **No .pkl write.**

Exports (≤13 chars): `portf_sum_tb`
"""
from __future__ import annotations

import pandas as pd


def portf_sum_tb(summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Last-stage portfolio table: shares, last close, value, net cash flow.
    Pass-through copy so callers can chain; empty in → empty out.
    """
    if summary_df is None or summary_df.empty:
        return pd.DataFrame()
    return summary_df.copy()
