"""
Build (samples, timesteps, features) and per-horizon y vectors. Time-based train/test.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import _u_entries as U
from ._2_fns_features import FEATURE_COLS


def horizon_key_to_target_col(key: str) -> str:
    return f"y_{key}"


def build_sequences_for_horizon(
    df: pd.DataFrame,
    horizon_key: str,
    timesteps: int | None = None,
    train_cutoff: pd.Timestamp | None = None,
    ticker_filter: str | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns X_train, y_train, X_test, y_test, sigma_test.

    Labels are **vol-normalized**: y = forward_return / max(vol_60d_raw, MIN_SIGMA)
    at the label date. Same scaling at predict (pred_return = pred * sigma).
    `sigma_test` aligns with X_test / y_test rows (test split only).
    """
    if timesteps is None:
        timesteps = U.timesteps_for_horizon(horizon_key)

    target_col = horizon_key_to_target_col(horizon_key)
    if target_col not in df.columns:
        raise KeyError(target_col)

    if train_cutoff is None:
        from ._2_fns_features import train_date_cutoff

        train_cutoff = train_date_cutoff(df, U.TRAIN_FRAC)

    X_train_list: list[np.ndarray] = []
    y_train_list: list[float] = []
    X_test_list: list[np.ndarray] = []
    y_test_list: list[float] = []
    sigma_test_list: list[float] = []

    if U.VOL_ANCHOR_COL not in df.columns:
        raise KeyError(
            f"Missing {U.VOL_ANCHOR_COL}; add_features/prepare_ml_frame must set raw vol anchor."
        )

    tick_loop = [ticker_filter] if ticker_filter is not None else list(df["ticker"].unique())
    for t in tick_loop:
        sub = df[df["ticker"] == t].sort_values("date").reset_index(drop=True)
        if len(sub) < timesteps:
            continue
        feat = sub[FEATURE_COLS].to_numpy(dtype=np.float64)
        yv = sub[target_col].to_numpy(dtype=np.float64)
        sig_raw = sub[U.VOL_ANCHOR_COL].to_numpy(dtype=np.float64)
        dates = sub["date"].to_numpy()

        for i in range(timesteps - 1, len(sub)):
            if not np.all(np.isfinite(feat[i - timesteps + 1 : i + 1])):
                continue
            if not np.isfinite(yv[i]) or not np.isfinite(sig_raw[i]):
                continue
            sig = max(float(sig_raw[i]), float(U.MIN_SIGMA_FOR_TARGET))
            y_norm = float(yv[i]) / sig
            if not np.isfinite(y_norm):
                continue
            window = feat[i - timesteps + 1 : i + 1]
            end_date = pd.Timestamp(dates[i])
            if end_date <= train_cutoff:
                X_train_list.append(window)
                y_train_list.append(y_norm)
            else:
                X_test_list.append(window)
                y_test_list.append(y_norm)
                sigma_test_list.append(sig)

    if not X_train_list:
        raise ValueError("No training sequences; check data length / cutoff / NaNs.")

    n_feat = len(FEATURE_COLS)
    X_train = np.stack(X_train_list, axis=0)
    y_train = np.asarray(y_train_list, dtype=np.float64)
    X_test = (
        np.stack(X_test_list, axis=0)
        if X_test_list
        else np.empty((0, timesteps, n_feat))
    )
    y_test = np.asarray(y_test_list, dtype=np.float64) if y_test_list else np.empty((0,))
    sigma_test = (
        np.asarray(sigma_test_list, dtype=np.float64)
        if sigma_test_list
        else np.empty((0,))
    )

    return X_train, y_train, X_test, y_test, sigma_test


def last_window_for_prediction(
    df: pd.DataFrame,
    ticker: str,
    horizon_key: str,
) -> np.ndarray | None:
    """Shape (1, timesteps, n_features); timesteps depend on horizon."""
    timesteps = U.timesteps_for_horizon(horizon_key)
    sub = df[df["ticker"] == ticker].sort_values("date").reset_index(drop=True)
    if len(sub) < timesteps:
        return None
    feat = sub[FEATURE_COLS].to_numpy(dtype=np.float64)
    i = len(sub) - 1
    w = feat[i - timesteps + 1 : i + 1]
    if not np.all(np.isfinite(w)):
        return None
    return w[np.newaxis, ...]
