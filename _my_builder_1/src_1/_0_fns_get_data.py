"""
ONLY module that writes `.pkl`. Incremental Yahoo OHLCV sync → `_dta_raw_fetched.pkl`.

Export: `sync_raw_pkl` (11 chars).

- If pickle **missing** → fetch all `entries.FETCH_STOCKS`, save, return df.
- If pickle **exists** and has every requested ticker → **load only** (no network).
- If **new** symbols appear in `FETCH_STOCKS` → fetch **only those**, **merge** columns, save, return df.
"""
from __future__ import annotations

import warnings
from pathlib import Path
from typing import Literal, Sequence

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError as e:  # pragma: no cover
    raise ImportError("Install yfinance: pip install yfinance") from e

from . import entries

# Fixed filename next to this package (do not rename casually — notebook + run rely on it)
DTA_RAW_PKL = "_dta_raw_fetched.pkl"

YF_YEARS: float | int = 5
YF_FILL: Literal["ffill", "hybrid", "linear"] = "hybrid"
YF_LEADING: Literal["keep", "nan_until_first_trade"] = "nan_until_first_trade"
YF_RAW_OHLC: bool = True
YF_END: str | pd.Timestamp | None = None

_TRUTH = ("Open", "High", "Low", "Close", "Adj Close", "Volume")


def default_raw_pkl_path() -> Path:
    """Absolute path to `DTA_RAW_PKL` next to these modules (independent of cwd)."""
    return Path(__file__).resolve().parent / DTA_RAW_PKL


def _norm_sym(s: str) -> str:
    return str(s).strip().upper()


def _panel_ok(df: pd.DataFrame | None) -> bool:
    if df is None or df.empty:
        return False
    if not isinstance(df.columns, pd.MultiIndex):
        return False
    lev0 = df.columns.get_level_values(0)
    return len(lev0) > 0 and all(isinstance(c, str) for c in lev0[: min(3, len(lev0))])


def _have_syms(df: pd.DataFrame) -> set[str]:
    return {_norm_sym(x) for x in df.columns.get_level_values(0).unique()}


def _merge_wide(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """Horizontally concat two wide MultiIndex panels on union index (sorted)."""
    if left is None or left.empty:
        return right.copy() if right is not None else pd.DataFrame()
    if right is None or right.empty:
        return left.copy()
    ix = left.index.union(right.index).sort_values()
    a = left.reindex(ix)
    b = right.reindex(ix)
    out = pd.concat([a, b], axis=1)
    out.index.name = "date"
    return out


def _dl_ohlcv(tickers: list[str], *, start: str, end: str, raw_ohlc: bool) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for t in tickers:
        block = _one_sym(t, start=start, end=end, raw_ohlc=raw_ohlc)
        if block.empty:
            block = pd.DataFrame(columns=list(_TRUTH))
        block.columns = pd.MultiIndex.from_product([[t], block.columns])
        parts.append(block)
    if not parts:
        return pd.DataFrame(columns=pd.MultiIndex.from_product([tickers, list(_TRUTH)]))
    return pd.concat(parts, axis=1)


def _one_sym(ticker: str, *, start: str, end: str, raw_ohlc: bool) -> pd.DataFrame:
    try:
        t = yf.Ticker(ticker)
        h = t.history(start=start, end=end, auto_adjust=not raw_ohlc, repair=True)
    except Exception:
        return pd.DataFrame()
    if h is None or h.empty:
        return pd.DataFrame()
    idx = pd.to_datetime(h.index).tz_localize(None).normalize()
    h = h.copy()
    h.index = idx
    h = h[~h.index.duplicated(keep="last")]
    out = pd.DataFrame(index=h.index)
    for name in _TRUTH:
        out[name] = pd.to_numeric(h[name], errors="coerce") if name in h.columns else np.nan
    if "Adj Close" not in h.columns:
        out["Adj Close"] = out["Close"]
    return out[list(_TRUTH)]


def _yf_panel_df(
    stocks: Sequence[str],
    years_back: float | int,
    *,
    end: str | pd.Timestamp | None,
    fill: Literal["ffill", "hybrid", "linear"],
    leading: Literal["keep", "nan_until_first_trade"],
    raw_ohlc: bool,
) -> pd.DataFrame:
    if not stocks:
        return pd.DataFrame()
    tickers = [str(s).strip() for s in stocks if str(s).strip()]
    end_ts = pd.Timestamp(end or pd.Timestamp.utcnow().normalize()).tz_localize(None).normalize()
    yb = float(years_back)
    start_ts = (end_ts - pd.DateOffset(months=int(round(yb * 12)))).normalize()
    calendar = pd.date_range(start=start_ts, end=end_ts, freq="D")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wide = _dl_ohlcv(
            tickers,
            start=start_ts.strftime("%Y-%m-%d"),
            end=(end_ts + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            raw_ohlc=raw_ohlc,
        )
    out = wide.reindex(calendar)
    price_fields = [f for f in _TRUTH if f != "Volume"]
    for t in tickers:
        for f in price_fields:
            col = (t, f)
            if col not in out.columns:
                continue
            # Bad/missing Yahoo data can leave object dtype; interpolate requires float.
            s = pd.to_numeric(out[col], errors="coerce")
            if fill == "ffill":
                out[col] = s.ffill()
            elif fill == "hybrid":
                s = s.ffill()
                out[col] = s.interpolate(method="time", limit_area="inside", axis=0)
            elif fill == "linear":
                out[col] = s.interpolate(method="time", limit_direction="both", axis=0)
            else:
                raise ValueError(f"Unknown fill={fill!r}")
    for t in tickers:
        cl, vo = (t, "Close"), (t, "Volume")
        if cl not in out.columns or vo not in out.columns:
            continue
        out[cl] = pd.to_numeric(out[cl], errors="coerce")
        has_px = out[cl].notna()
        out[vo] = pd.to_numeric(out[vo], errors="coerce")
        out.loc[has_px, vo] = out.loc[has_px, vo].fillna(0.0)
    if leading not in ("keep", "nan_until_first_trade"):
        raise ValueError(f"Unknown leading={leading!r}")
    out.index.name = "date"
    return out


def sync_raw_pkl(
    pkl_path: str | Path | None = None,
    *,
    tickers: Sequence[str] | None = None,
    force_full: bool = False,
    years_back: float | int | None = None,
    end: str | pd.Timestamp | None = None,
    fill: Literal["ffill", "hybrid", "linear"] | None = None,
    leading: Literal["keep", "nan_until_first_trade"] | None = None,
    raw_ohlc: bool | None = None,
    verbose: bool = True,
) -> tuple[Path, pd.DataFrame]:
    """
    Load or update `_dta_raw_fetched.pkl`. Returns ``(path, dataframe)``.

    - **force_full**: ignore pickle and refetch all `tickers` (default ``FETCH_STOCKS``).
    """
    if pkl_path is None:
        pkl_path = default_raw_pkl_path()
    if tickers is None:
        tickers = list(entries.FETCH_STOCKS)
    want_syms = [_norm_sym(t) for t in tickers if str(t).strip()]
    want_syms = list(dict.fromkeys(want_syms))  # preserve order, upper for matching
    # map upper -> display symbol from entries order
    sym_display: dict[str, str] = {}
    for t in tickers:
        u = _norm_sym(t)
        if u and u not in sym_display:
            sym_display[u] = str(t).strip()

    if years_back is None:
        years_back = YF_YEARS
    if end is None:
        end = YF_END
    if fill is None:
        fill = YF_FILL
    if leading is None:
        leading = YF_LEADING
    if raw_ohlc is None:
        raw_ohlc = YF_RAW_OHLC

    out = Path(pkl_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    def _msg(*a: object) -> None:
        if verbose:
            print(*a)

    if not want_syms:
        df_empty = pd.DataFrame()
        df_empty.to_pickle(out)
        _msg("[sync_raw_pkl] FETCH_STOCKS empty → wrote empty pickle.")
        return out, df_empty

    if force_full:
        fetch_list = [sym_display[u] for u in want_syms]
        df = _yf_panel_df(
            fetch_list,
            years_back,
            end=end,
            fill=fill,
            leading=leading,
            raw_ohlc=raw_ohlc,
        )
        df.to_pickle(out)
        _msg(
            f"Full refetch (force_full=True): {fetch_list} → saved {out.name} shape={df.shape}"
        )
        return out, df

    if not out.exists():
        fetch_list = [sym_display[u] for u in want_syms]
        df = _yf_panel_df(
            fetch_list,
            years_back,
            end=end,
            fill=fill,
            leading=leading,
            raw_ohlc=raw_ohlc,
        )
        df.to_pickle(out)
        _msg(
            f"No pickle yet — full fetch from Yahoo: {fetch_list} → saved {out.name} shape={df.shape}"
        )
        return out, df

    try:
        existing = pd.read_pickle(out)
    except Exception as e:
        _msg(f"Pickle unreadable ({e!r}) — full refetch from Yahoo.")
        fetch_list = [sym_display[u] for u in want_syms]
        df = _yf_panel_df(
            fetch_list,
            years_back,
            end=end,
            fill=fill,
            leading=leading,
            raw_ohlc=raw_ohlc,
        )
        df.to_pickle(out)
        _msg(f"Saved {out.name} shape={df.shape}")
        return out, df

    if not _panel_ok(existing):
        _msg("Pickle invalid shape — full refetch from Yahoo.")
        fetch_list = [sym_display[u] for u in want_syms]
        df = _yf_panel_df(
            fetch_list,
            years_back,
            end=end,
            fill=fill,
            leading=leading,
            raw_ohlc=raw_ohlc,
        )
        df.to_pickle(out)
        _msg(f"Saved {out.name} shape={df.shape}")
        return out, df

    have = _have_syms(existing)
    missing_u = [u for u in want_syms if u not in have]

    if not missing_u:
        _msg(
            f'No new data — using imported pickle only: "{out.name}" '
            f"({len(want_syms)} symbol(s) already present)."
        )
        return out, existing

    fetch_list = [sym_display[u] for u in missing_u]
    _msg(
        f"Fetched NEW ticker(s) from Yahoo and merged into pickle: {fetch_list} → saved {out.name}"
    )
    fresh = _yf_panel_df(
        fetch_list,
        years_back,
        end=end,
        fill=fill,
        leading=leading,
        raw_ohlc=raw_ohlc,
    )
    merged = _merge_wide(existing, fresh)
    merged.to_pickle(out)
    _msg(f"Updated panel shape: {merged.shape}")
    return out, merged
