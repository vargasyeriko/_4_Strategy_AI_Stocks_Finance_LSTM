"""
Feature engineering (past-only) + per-ticker StandardScaler fit on train, transform all.

Uses numpy for scaling so scikit-learn is optional.
"""
from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from . import _u_entries as U

# Per-ticker z-scored after train cutoff (own history; comparable dynamics per symbol)
PER_TICKER_SCALE_COLS: list[str] = [
    "ret_1d",
    "ret_5d",
    "ret_20d",
    "ma_20",
    "ma_50",
    "vol_20d",
    "vol_60d",
    "vol_252d",
    "rv_log_20_60",
    "rv_log_60_252",
]

# Cross-sectional volatility rank per calendar date (0 = calm vs peers, 1 = most volatile
# among names trading that day). Globally z-scored on train rows only — not per-ticker scaled.
VOL_RANK_COLS: list[str] = [
    "vol_rank_xs_60d",
    "vol_rank_xs_252d",
]

# Full LSTM input order (must match sequence builder)
FEATURE_COLS: list[str] = PER_TICKER_SCALE_COLS + VOL_RANK_COLS


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Past-only features per ticker.

    Volatility stack:
      - Multi-window realized vol (20d / 60d / ~1y) for level and term structure.
      - Log ratios log(vol_short/vol_long): stress when recent vol exceeds long-run vol.
      - vol_rank_xs_*: percentile rank of that vol among all tickers on the same date
        (high vs low volatility names on the same day — train z-score applied later).
    """
    eps = 1e-12
    out = df.sort_values(["ticker", "date"]).copy()
    g = out.groupby("ticker", group_keys=False)

    out["ret_1d"] = g["close"].transform(lambda s: s.pct_change(1))
    out["ret_5d"] = g["close"].transform(lambda s: s / s.shift(5) - 1.0)
    out["ret_20d"] = g["close"].transform(lambda s: s / s.shift(20) - 1.0)

    out["ma_20"] = g["close"].transform(lambda s: s.rolling(20, min_periods=20).mean())
    out["ma_50"] = g["close"].transform(lambda s: s.rolling(50, min_periods=50).mean())

    out["vol_20d"] = g["ret_1d"].transform(lambda s: s.rolling(20, min_periods=20).std())
    out["vol_60d"] = g["ret_1d"].transform(lambda s: s.rolling(60, min_periods=60).std())
    out["vol_252d"] = g["ret_1d"].transform(
        lambda s: s.rolling(252, min_periods=252).std()
    )

    v20 = out["vol_20d"]
    v60 = out["vol_60d"]
    v252 = out["vol_252d"]
    out["rv_log_20_60"] = np.log((v20 + eps) / (v60 + eps))
    out["rv_log_60_252"] = np.log((v60 + eps) / (v252 + eps))

    def _pct_rank(s: pd.Series) -> pd.Series:
        return s.rank(pct=True, method="average")

    out["vol_rank_xs_60d"] = out.groupby("date", group_keys=False)["vol_60d"].transform(
        _pct_rank
    )
    out["vol_rank_xs_252d"] = out.groupby("date", group_keys=False)["vol_252d"].transform(
        _pct_rank
    )

    # Unscaled copy for target = return / vol (per-ticker z-scoring below must not touch this)
    out["vol_60d_raw"] = out["vol_60d"].astype(np.float64)

    return out


def apply_vol_rank_global_zscore_train_only(
    df: pd.DataFrame,
    cutoff: pd.Timestamp,
    cols: list[str] | None = None,
) -> dict[str, tuple[float, float]]:
    """
    In-place: z-score VOL_RANK columns using mean/std from rows with date <= cutoff only.
    Returns {col: (mean, std)} for inspection or persistence.
    """
    cols = cols or VOL_RANK_COLS
    stats: dict[str, tuple[float, float]] = {}
    tr = df[df["date"] <= cutoff]
    for c in cols:
        mu = float(np.nanmean(tr[c].to_numpy(dtype=np.float64)))
        sd = float(np.nanstd(tr[c].to_numpy(dtype=np.float64)))
        sd = max(sd, 1e-12)
        stats[c] = (mu, sd)
        df[c] = (df[c] - mu) / sd
    return stats


def apply_horizon_training_window(df: pd.DataFrame, horizon_key: str) -> pd.DataFrame:
    """
    Use last ~1 calendar year for short horizons (3d/7d/30d), ~3 years for 90d/180d.
    Falls back to full `df` if the slice would be tiny.
    """
    if df.empty:
        return df
    mx = pd.Timestamp(df["date"].max())
    if horizon_key in U.SHORT_HORIZONS_FOR_WINDOW:
        mn = mx - pd.DateOffset(years=U.TRAINING_WINDOW_YEARS_SHORT)
    else:
        mn = mx - pd.DateOffset(years=U.TRAINING_WINDOW_YEARS_LONG)
    out = df[df["date"] >= mn].copy()
    if len(out) < 80:
        return df
    return out


def train_date_cutoff(df: pd.DataFrame, train_frac: float = U.TRAIN_FRAC) -> pd.Timestamp:
    """Global time cutoff: last train_frac of *unique dates* (sorted)."""
    dates = np.sort(df["date"].unique())
    n = max(1, int(len(dates) * train_frac))
    return pd.Timestamp(dates[n - 1])


@dataclass
class PerTickerScaler:
    """Per-feature mean/std on train rows; transform any subset."""

    means: dict[str, np.ndarray] = field(default_factory=dict)
    stds: dict[str, np.ndarray] = field(default_factory=dict)

    def fit(self, ticker: str, X: np.ndarray) -> None:
        """X shape (n_rows, n_features)."""
        mu = np.nanmean(X, axis=0)
        sd = np.nanstd(X, axis=0)
        sd = np.where(sd < 1e-12, 1.0, sd)
        self.means[ticker] = mu.astype(np.float64)
        self.stds[ticker] = sd.astype(np.float64)

    def transform(self, ticker: str, X: np.ndarray) -> np.ndarray:
        mu = self.means[ticker]
        sd = self.stds[ticker]
        return (X - mu) / sd


def fit_scalers_train_only(
    df: pd.DataFrame,
    feature_cols: list[str],
    cutoff: pd.Timestamp,
) -> PerTickerScaler:
    """Fit scaler per ticker using rows with date <= cutoff only."""
    scaler = PerTickerScaler()
    for t in df["ticker"].unique():
        sub = df[(df["ticker"] == t) & (df["date"] <= cutoff)]
        if sub.empty:
            continue
        X = sub[feature_cols].to_numpy(dtype=np.float64)
        scaler.fit(str(t), X)
    return scaler


def transform_features_df(
    df: pd.DataFrame,
    per_ticker_cols: list[str],
    scaler: PerTickerScaler,
) -> pd.DataFrame:
    """Return copy with per-ticker z-scored columns (VOL_RANK_COLS unchanged)."""
    out = df.copy()
    for t in out["ticker"].unique():
        ts = str(t)
        if ts not in scaler.means:
            continue
        m = out["ticker"] == t
        X = out.loc[m, per_ticker_cols].to_numpy(dtype=np.float64)
        out.loc[m, per_ticker_cols] = scaler.transform(ts, X)
    return out


def save_scalers(scaler: PerTickerScaler, path: Path | None = None) -> Path:
    path = path or (U.SAVED_MODELS_DIR / U.SCALERS_NAME)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"means": scaler.means, "stds": scaler.stds}, f)
    return path


def load_scalers(path: Path | None = None) -> PerTickerScaler:
    path = path or (U.SAVED_MODELS_DIR / U.SCALERS_NAME)
    with open(path, "rb") as f:
        payload = pickle.load(f)
    sc = PerTickerScaler()
    sc.means = payload["means"]
    sc.stds = payload["stds"]
    return sc


def tickers_eligible_for_ml() -> list[str]:
    """
    Tickers that survive targets + features + row dropna and have >= MIN_ROWS_PER_TICKER rows.
    Use this for the predict menu so users only pick symbols that will actually work.
    """
    from ._0_fns_io import load_panel_long
    from ._1_fns_targets import add_return_targets

    df = load_panel_long()
    df = add_return_targets(df)
    df = add_features(df)
    df = df.dropna(
        subset=FEATURE_COLS + U.TARGET_COLS + [U.VOL_ANCHOR_COL], how="any"
    )
    counts = df.groupby("ticker").size()
    ok = set(counts[counts >= U.MIN_ROWS_PER_TICKER].index.astype(str).str.upper())
    prim = [t for t in U.STOCKS if t in ok]
    rest = sorted(ok - set(prim))
    return prim + rest


def prepare_ml_frame(ticker_allowlist: list[str] | None = None):
    """
    Load PKL → targets → features → drop NaNs → per-ticker train scalers → scaled frame.
    Returns (df_scaled, scaler, train_cutoff).
    """
    from ._0_fns_io import load_panel_long
    from ._1_fns_targets import add_return_targets

    df = load_panel_long()
    if ticker_allowlist is not None:
        allow = {str(x).upper().strip() for x in ticker_allowlist}
        df = df[df["ticker"].isin(allow)]

    df = add_return_targets(df)
    df = add_features(df)
    df = df.dropna(subset=FEATURE_COLS + U.TARGET_COLS + [U.VOL_ANCHOR_COL], how="any")

    counts = df.groupby("ticker").size()
    keep = counts[counts >= U.MIN_ROWS_PER_TICKER].index
    df = df[df["ticker"].isin(keep)].reset_index(drop=True)

    if df.empty:
        raise ValueError("No rows left after filters; lower MIN_ROWS_PER_TICKER or check PKL.")

    cutoff = train_date_cutoff(df, U.TRAIN_FRAC)
    apply_vol_rank_global_zscore_train_only(df, cutoff)
    scaler = fit_scalers_train_only(df, PER_TICKER_SCALE_COLS, cutoff)
    df_scaled = transform_features_df(df, PER_TICKER_SCALE_COLS, scaler)
    return df_scaled, scaler, cutoff
