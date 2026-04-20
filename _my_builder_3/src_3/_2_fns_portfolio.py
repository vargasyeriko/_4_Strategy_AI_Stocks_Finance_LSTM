"""Target allocation — growth vs defensive buckets."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ._u_entries import (
    DEFENSIVE_TICKERS,
    GROWTH_TICKERS,
    TARGET_WEIGHT_DEFENSIVE,
    TARGET_WEIGHT_GROWTH,
)


@dataclass(frozen=True)
class BucketWeights:
    symbols: list[str]
    weights: dict[str, float]


def _intersect_available(requested: list[str], available: list[str]) -> list[str]:
    av = set(available)
    return [s for s in requested if s in av]


def equal_weight(names: list[str]) -> dict[str, float]:
    if not names:
        return {}
    w = 1.0 / len(names)
    return {n: w for n in names}


def build_bucket_weights(available_tickers: list[str]) -> tuple[BucketWeights, BucketWeights]:
    g_syms = _intersect_available(GROWTH_TICKERS, available_tickers)
    d_syms = _intersect_available(DEFENSIVE_TICKERS, available_tickers)
    return (
        BucketWeights(g_syms, equal_weight(g_syms)),
        BucketWeights(d_syms, equal_weight(d_syms)),
    )


def global_target_weights(
    growth: BucketWeights,
    defensive: BucketWeights,
) -> dict[str, float]:
    wg = TARGET_WEIGHT_GROWTH
    wd = TARGET_WEIGHT_DEFENSIVE
    if abs(wg + wd - 1.0) > 1e-6:
        raise ValueError("TARGET_WEIGHT_GROWTH + TARGET_WEIGHT_DEFENSIVE must equal 1.0")
    out: dict[str, float] = {}
    for s, w in growth.weights.items():
        out[s] = out.get(s, 0.0) + wg * w
    for s, w in defensive.weights.items():
        out[s] = out.get(s, 0.0) + wd * w
    return dict(sorted(out.items(), key=lambda x: -x[1]))


def last_row(close: pd.DataFrame) -> pd.Series:
    return close.iloc[-1]


def notionals_at_last(
    close: pd.DataFrame,
    target_weights: dict[str, float],
    capital: float = 100_000.0,
) -> pd.Series:
    last = last_row(close)
    return pd.Series({k: target_weights[k] * capital for k in target_weights if k in last.index})
