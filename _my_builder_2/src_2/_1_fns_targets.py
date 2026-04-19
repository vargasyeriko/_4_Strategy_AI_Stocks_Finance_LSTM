"""
Future return targets per ticker (no leakage: targets use future closes only in label column).
"""
from __future__ import annotations

import pandas as pd

from . import _u_entries as U


def add_return_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each ticker:
      y_k = close.shift(-k) / close - 1
    Drops nothing here — drop NaN targets later after features.
    """
    out = df.copy()
    g = out.groupby("ticker", group_keys=False)
    for name, k in U.HORIZON_DAYS.items():
        col = f"y_{name}"
        out[col] = g["close"].transform(lambda s: s.shift(-k) / s - 1.0)
    return out


def drop_rows_missing_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where any horizon target is NaN."""
    sub = df.dropna(subset=U.TARGET_COLS, how="any").reset_index(drop=True)
    return sub
