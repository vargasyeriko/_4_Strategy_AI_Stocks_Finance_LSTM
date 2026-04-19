"""
Load pickle panel, enforce long schema: date, ticker, close, (+ OHLCV for features).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REQUIRED_LONG = ["date", "ticker", "close"]


def load_pkl(path: str | Path) -> pd.DataFrame:
    """Load pandas object from pickle (path under src_2/data/)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    obj: Any = pd.read_pickle(path)
    if not isinstance(obj, pd.DataFrame):
        raise TypeError(f"Expected DataFrame, got {type(obj)}")
    return obj


def wide_panel_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert MultiIndex wide panel (date index × (ticker, field)) to long format.
    Output columns include open, high, low, close, volume (lowercase) when present.
    """
    if not isinstance(df.columns, pd.MultiIndex):
        # Already long-ish or flat
        out = df.copy()
        if "date" not in out.columns and isinstance(out.index, pd.DatetimeIndex):
            out = out.reset_index().rename(columns={out.index.name or "index": "date"})
        return _normalize_long_columns(out)

    # Wide: columns level 0 = ticker, level 1 = field name
    try:
        stacked = df.stack(level=0, future_stack=True)
    except TypeError:
        stacked = df.stack(level=0)
    stacked.index.names = ["date", "ticker"]
    out = stacked.reset_index()
    return _normalize_long_columns(out)


def _normalize_long_columns(df: pd.DataFrame) -> pd.DataFrame:
    colmap = {c: str(c).strip().lower() for c in df.columns}
    df = df.rename(columns=colmap)
    # Standard names
    for old, new in [("adj close", "adj_close"), ("adj_close", "adj_close")]:
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})
    if "close" not in df.columns:
        raise ValueError("Long frame must contain 'close'")
    df["date"] = pd.to_datetime(df["date"])
    df["ticker"] = df["ticker"].astype("string").str.upper().str.strip()
    # Sort
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    return df


def enforce_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Validate required columns; index as RangeIndex (date in column)."""
    missing = [c for c in REQUIRED_LONG if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["ticker"] = df["ticker"].astype("string").str.upper()
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    return df


def load_panel_long(path: str | Path | None = None) -> pd.DataFrame:
    """
    End-to-end: read PKL, reshape wide → long, enforce structure.
    `path` defaults to first match: `_dta_raw_fetched*.pkl` or `data/your_data.pkl` in src_2.
    """
    if path is None:
        from ._u_entries import resolve_data_pkl

        p = resolve_data_pkl()
    else:
        p = Path(path)
    raw = load_pkl(p)
    if isinstance(raw.columns, pd.MultiIndex):
        long_df = wide_panel_to_long(raw)
    else:
        long_df = enforce_structure(raw)
    long_df = enforce_structure(long_df)
    # Drop rows with invalid close
    long_df = long_df[np.isfinite(long_df["close"].astype(float))]
    long_df = long_df[long_df["close"] > 0]
    return long_df.reset_index(drop=True)
