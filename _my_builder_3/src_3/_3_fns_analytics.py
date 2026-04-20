"""Risk / return stats on the close matrix + growth vs defensive equity curves over time."""
from __future__ import annotations

import numpy as np
import pandas as pd


def daily_returns(close: pd.DataFrame) -> pd.DataFrame:
    return close.sort_index().pct_change().dropna(how="all")


def annualized_vol(returns: pd.DataFrame, trading_days: int = 252) -> pd.Series:
    return returns.std() * np.sqrt(trading_days)


def total_return(close: pd.DataFrame) -> pd.Series:
    c = close.sort_index()
    first = c.apply(lambda s: s.dropna().iloc[0] if s.dropna().shape[0] else np.nan)
    last = c.iloc[-1]
    return (last / first) - 1.0


def describe_universe(close: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    sub = close[[t for t in tickers if t in close.columns]]
    r = daily_returns(sub)
    vol = annualized_vol(r)
    tr = total_return(sub)
    out = pd.DataFrame({"last": sub.iloc[-1], "ann_vol": vol, "total_ret": tr})
    return out.sort_values("last", ascending=False)


# --- Growth vs defensive: equal-weight buy-and-hold within bucket -----------------


def equity_curve_equal_weight(close: pd.DataFrame, tickers: list[str]) -> pd.Series:
    """
    $1 split equally across names at the first row where all bucket names have prices
    (after forward-fill). Series is portfolio value over time, starts at 1.0.
    """
    cols = [t for t in tickers if t in close.columns]
    if not cols:
        return pd.Series(dtype=float)
    sub = close[cols].sort_index().ffill()
    sub = sub.dropna(how="any")
    if sub.empty or len(sub) < 2:
        return pd.Series(dtype=float)
    norm = sub / sub.iloc[0]
    return norm.mean(axis=1).rename("equal_weight_bh")


def blend_bucket_curves(
    eq_growth: pd.Series,
    eq_defensive: pd.Series,
    weight_growth: float,
    weight_defensive: float,
) -> pd.Series:
    """Align on common dates; blend starts near 1.0 (rebased so initial = 1)."""
    df = pd.concat([eq_growth, eq_defensive], axis=1, keys=["g", "d"]).dropna(how="any")
    if df.empty:
        return pd.Series(dtype=float)
    blend = weight_growth * df["g"] + weight_defensive * df["d"]
    return (blend / blend.iloc[0]).rename("blend_target_mix")


def max_drawdown(eq: pd.Series) -> float:
    if eq.empty or len(eq) < 2:
        return float("nan")
    peak = eq.cummax()
    return float((eq / peak - 1.0).min())


def cagr_from_equity(eq: pd.Series) -> float:
    """CAGR from first to last index date, using ending equity vs start (=1)."""
    if eq.empty or len(eq) < 2:
        return float("nan")
    end = float(eq.iloc[-1])
    days = (eq.index[-1] - eq.index[0]).days
    if days <= 0:
        return float("nan")
    years = days / 365.25
    return end ** (1.0 / years) - 1.0


def ann_vol_of_equity(eq: pd.Series, trading_days: int = 252) -> float:
    """Vol of daily returns of the equity curve."""
    if eq.empty or len(eq) < 3:
        return float("nan")
    r = eq.pct_change().dropna()
    return float(r.std() * np.sqrt(trading_days))


def build_bucket_equity_frame(
    close: pd.DataFrame,
    growth_syms: list[str],
    defensive_syms: list[str],
    weight_growth: float,
    weight_defensive: float,
) -> pd.DataFrame:
    """
    Columns: ``Growth``, ``Defensive`` (if both exist), ``Blend`` — normalized to 1.0
    at the first row of the aligned window.
    """
    eg = equity_curve_equal_weight(close, growth_syms)
    ed = equity_curve_equal_weight(close, defensive_syms)
    if eg.empty and ed.empty:
        return pd.DataFrame()

    parts: dict[str, pd.Series] = {}
    if not eg.empty:
        parts["Growth"] = eg
    if not ed.empty:
        parts["Defensive"] = ed

    if len(parts) == 2:
        merged = pd.concat(parts, axis=1).dropna(how="any")
        if merged.empty:
            return pd.DataFrame()
        merged["Growth"] = merged["Growth"] / merged["Growth"].iloc[0]
        merged["Defensive"] = merged["Defensive"] / merged["Defensive"].iloc[0]
        merged["Blend"] = weight_growth * merged["Growth"] + weight_defensive * merged["Defensive"]
        merged["Blend"] = merged["Blend"] / merged["Blend"].iloc[0]
        return merged

    name, s = next(iter(parts.items()))
    s = s.dropna()
    if s.empty:
        return pd.DataFrame()
    out = pd.DataFrame({name: s / s.iloc[0]})
    out["Blend"] = out[name]
    return out


def bucket_performance_summary(eq_frame: pd.DataFrame) -> pd.DataFrame:
    """One row per bucket: total return, CAGR, ann vol, max DD."""
    if eq_frame.empty:
        return pd.DataFrame()
    rows = []
    for col in eq_frame.columns:
        s = eq_frame[col].dropna()
        if len(s) < 2:
            continue
        tot = float(s.iloc[-1] / s.iloc[0] - 1.0)
        rows.append(
            {
                "bucket": col,
                "total_return": tot,
                "cagr": cagr_from_equity(s),
                "ann_vol": ann_vol_of_equity(s),
                "max_drawdown": max_drawdown(s),
                "start": s.index[0],
                "end": s.index[-1],
            }
        )
    return pd.DataFrame(rows).set_index("bucket")
