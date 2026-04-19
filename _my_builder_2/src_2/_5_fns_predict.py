"""
Load trained models + scalers; emit prediction table(s).

Inference uses model(x, training=False) + optional model cache to reduce TF noise.
"""
from __future__ import annotations

import logging
import os
import sys
import warnings
from typing import Any

import numpy as np
import pandas as pd

from . import _u_entries as U
from ._3_fns_sequences import last_window_for_prediction
from ._4_fns_models import load_model


def suppress_tensorflow_predict_noise() -> None:
    """Call before inference; TF is usually already imported by _4."""
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
    logging.getLogger("tensorflow").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", message=".*[Rr]etracing.*")
    warnings.filterwarnings("ignore", message=".*tf\\.function.*")
    warnings.filterwarnings("ignore", category=UserWarning, module="tensorflow")
    try:
        import absl.logging

        absl.logging.set_verbosity(absl.logging.ERROR)
    except Exception:
        pass
    try:
        import tensorflow as tf

        tf.get_logger().setLevel(logging.ERROR)
    except Exception:
        pass


def pred_column_name(horizon_key: str) -> str:
    return f"pred_{horizon_key}"


def predict_last_window(
    df_scaled: pd.DataFrame,
    ticker: str,
    horizon_keys: list[str] | None = None,
    model_cache: dict[tuple[str, str], Any] | None = None,
    *,
    skip_stale_models: bool = True,
    skip_notes: list[str] | None = None,
) -> pd.DataFrame:
    """
    One row: date, ticker, pred_* …
    `model_cache` optional: reuse loaded models across tickers/horizons in one run.
    If `skip_stale_models`, horizons whose .keras file does not match the current
    architecture get NaN and a line is appended to `skip_notes` (if provided).
    """
    horizon_keys = horizon_keys or list(U.HORIZON_DAYS.keys())
    sub = df_scaled[df_scaled["ticker"] == ticker].sort_values("date")
    if sub.empty:
        raise ValueError(f"No rows for ticker {ticker!r}")
    last_date = sub["date"].iloc[-1]
    if U.VOL_ANCHOR_COL not in sub.columns:
        raise KeyError(f"Missing {U.VOL_ANCHOR_COL} for prediction scaling.")
    sig = max(float(sub[U.VOL_ANCHOR_COL].iloc[-1]), float(U.MIN_SIGMA_FOR_TARGET))

    row: dict = {"date": last_date, "ticker": ticker}
    cache = model_cache if model_cache is not None else {}
    t_up = str(ticker).strip().upper()

    for key in horizon_keys:
        w = last_window_for_prediction(df_scaled, ticker, key)
        if w is None:
            need = U.timesteps_for_horizon(key)
            raise ValueError(
                f"Insufficient history for {ticker!r} horizon {key} (need {need} rows)."
            )
        w32 = np.asarray(w, dtype=np.float32)
        mk = (t_up, key)
        if mk not in cache:
            try:
                cache[mk] = load_model(ticker, key)
            except ValueError as e:
                if skip_stale_models and "Stale model architecture" in str(e):
                    row[pred_column_name(key)] = float("nan")
                    if skip_notes is not None:
                        first = str(e).strip().split("\n")[0]
                        skip_notes.append(f"{t_up} / {key}: {first}")
                    continue
                raise
        m = cache[mk]
        out = m(w32, training=False)
        pred_n = float(np.asarray(out)[0, 0])
        row[pred_column_name(key)] = pred_n * sig

    return pd.DataFrame([row])


def collect_predictions_table(
    df_scaled: pd.DataFrame,
    tickers: list[str],
    horizon_keys: list[str],
    *,
    skip_stale_models: bool = True,
) -> tuple[pd.DataFrame, list[str]]:
    """All tickers in one frame; shared model cache. Returns (table, skip notes)."""
    suppress_tensorflow_predict_noise()
    cache: dict[tuple[str, str], Any] = {}
    rows: list[pd.DataFrame] = []
    skip_notes: list[str] = []
    for t in tickers:
        rows.append(
            predict_last_window(
                df_scaled,
                t,
                horizon_keys=horizon_keys,
                model_cache=cache,
                skip_stale_models=skip_stale_models,
                skip_notes=skip_notes,
            )
        )
    return pd.concat(rows, ignore_index=True), skip_notes


# ANSI (works in most terminals / iTerm / VS Code)
_RESET = "\033[0m"
_GREEN = "\033[32m"
_RED = "\033[31m"
_DIM = "\033[2m"


def format_pct_plain(x: float) -> str:
    return f"{100.0 * x:+.2f}%"


def print_predictions_table_colored(df: pd.DataFrame) -> None:
    """Single combined table; green = up, red = down (terminal only)."""
    if df is None or df.empty:
        print("(no predictions)")
        return

    pred_cols = [c for c in df.columns if c.startswith("pred_")]
    if not pred_cols:
        print("(no pred_* columns)")
        return

    use_color = sys.stdout.isatty()
    labels = [c.replace("pred_", "Pred_") for c in pred_cols]

    # header
    hdr = f"{'Date':<12}{'Ticker':<10}"
    for lab in labels:
        hdr += f"{lab:>12}"
    print(hdr)
    print("-" * len(hdr))

    for _, row in df.iterrows():
        d = str(row["date"])[:10]
        t = str(row["ticker"])[:9]
        line = f"{d:<12}{t:<10}"
        for c in pred_cols:
            v = row[c]
            if pd.isna(v):
                cell = f"{_DIM}{'—':>12}{_RESET}" if use_color else f"{'—':>12}"
                line += cell
                continue
            v = float(v)
            s = format_pct_plain(v)
            if use_color:
                if v > 0:
                    cell = f"{_GREEN}{s:>12}{_RESET}"
                elif v < 0:
                    cell = f"{_RED}{s:>12}{_RESET}"
                else:
                    cell = f"{_DIM}{s:>12}{_RESET}"
            else:
                cell = f"{s:>12}"
            line += cell
        print(line)
    print()


def format_pct(x: float) -> str:
    return format_pct_plain(x)
