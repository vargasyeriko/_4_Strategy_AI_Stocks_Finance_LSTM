"""
`_1_fns_history_by_symbol` — ledger + history tables. **No .pkl write.**

Exports (≤13 chars): `stk_ledg_df`, `hist_summ_pr`, `sym_hist_tb`
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from . import entries

_SPLIT_RX = re.compile(r"(\d+)\s*:\s*(\d+)")

LEDGER_COLS = [
    "date",
    "ticker",
    "kind",
    "shares",
    "split_ratio",
    "div_per_share",
    "reinvest",
    "price_per_share",
    "notes",
]


def _norm_row(r: dict) -> dict:
    out = {k: r.get(k, np.nan) for k in LEDGER_COLS}
    rv = out["reinvest"]
    if pd.isna(rv) or rv == "" or rv is None:
        out["reinvest"] = 0
    elif isinstance(rv, (bool, np.bool_)):
        out["reinvest"] = int(bool(rv))
    else:
        s = str(rv).strip().lower()
        out["reinvest"] = 1 if s in ("1", "true", "yes", "y") else 0
    if pd.isna(out.get("notes")):
        out["notes"] = ""
    return out


def _split_mult(s: str | float | None) -> float:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return 1.0
    if isinstance(s, (int, float)) and not isinstance(s, bool):
        return float(s)
    t = str(s).strip().replace(" ", "")
    if not t:
        return 1.0
    if ":" in t:
        a, b = t.split(":", 1)
        return float(a) / float(b)
    return float(t)


def _fmt_split(mult: float) -> str:
    if mult >= 1.0:
        return f"{mult:g}:1"
    return f"1:{1.0 / mult:g}"


def _sr_from_tx(tx: dict) -> str:
    sr = tx.get("split_ratio")
    if sr is not None and str(sr).strip():
        return str(sr).strip()
    desc = str(tx.get("description", ""))
    m = _SPLIT_RX.search(desc)
    if m:
        return f"{m.group(1)}:{m.group(2)}"
    return "1:1"


def _px_tx(tx: dict) -> float:
    v = tx.get("price_per_share")
    if v is None or v == "":
        return np.nan
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def _tx_row(tx: dict, sym: str) -> dict | None:
    typ = str(tx.get("type", "")).lower().strip()
    date = tx.get("date")
    if not date:
        return None
    base = {"date": date, "ticker": sym.upper(), "notes": ""}
    if typ == "buy":
        return {
            **base,
            "kind": "BUY",
            "shares": float(tx["shares"]),
            "split_ratio": np.nan,
            "div_per_share": np.nan,
            "reinvest": 0,
            "price_per_share": _px_tx(tx),
        }
    if typ == "sell":
        return {
            **base,
            "kind": "SELL",
            "shares": float(tx["shares"]),
            "split_ratio": np.nan,
            "div_per_share": np.nan,
            "reinvest": 0,
            "price_per_share": _px_tx(tx),
        }
    if typ == "split":
        return {
            **base,
            "kind": "SPLIT",
            "shares": np.nan,
            "split_ratio": _sr_from_tx(tx),
            "div_per_share": np.nan,
            "reinvest": 0,
            "price_per_share": np.nan,
        }
    if typ == "dividend":
        return {
            **base,
            "kind": "DIV",
            "shares": np.nan,
            "split_ratio": np.nan,
            "div_per_share": float(tx.get("amount", 0)),
            "reinvest": 1 if tx.get("reinvested") else 0,
            "price_per_share": np.nan,
        }
    return None


def stk_ledg_df(stock_hist: dict[str, list[dict]] | None = None) -> pd.DataFrame:
    """Ledger rows from user tx dicts (loops tickers). Empty `MY_STOCKS` → empty df, no crash."""
    if stock_hist is None:
        stock_hist = entries.MY_STOCKS
    if not stock_hist:
        return pd.DataFrame(columns=LEDGER_COLS)
    rows: list[dict] = []
    for sym in sorted(stock_hist.keys()):
        for tx in stock_hist[sym]:
            r = _tx_row(tx, str(sym).upper())
            if r:
                rows.append(_norm_row(r))
    if not rows:
        return pd.DataFrame(columns=LEDGER_COLS)
    led = pd.DataFrame(rows)
    led["date"] = pd.to_datetime(led["date"])
    led = led.sort_values(["date", "ticker", "kind"]).reset_index(drop=True)
    return led[LEDGER_COLS]


def _last_px(panel: pd.DataFrame | None, ticker: str) -> float | None:
    if panel is None or panel.empty:
        return None
    try:
        col = (ticker, "Close")
        if col not in panel.columns:
            return None
        s = panel[col].dropna()
        if s.empty:
            return None
        v = float(s.iloc[-1])
        return v if np.isfinite(v) else None
    except Exception:
        return None


def _px_on_day(panel: pd.DataFrame | None, ticker: str, dt: pd.Timestamp) -> float | None:
    if panel is None or panel.empty:
        return None
    dt = pd.Timestamp(dt).normalize()
    try:
        col = (ticker, "Close")
        if col not in panel.columns:
            return None
        s = panel[col]
        s = s[~s.index.duplicated(keep="last")].sort_index()
        if dt in s.index and pd.notna(s.loc[dt]):
            v = float(s.loc[dt])
            return v if np.isfinite(v) else None
        sub = s.loc[:dt].dropna()
        if sub.empty:
            return None
        v = float(sub.iloc[-1])
        return v if np.isfinite(v) else None
    except Exception:
        return None


def _led_run_ix(
    ledger: pd.DataFrame,
    price_panel: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if ledger is None or ledger.empty:
        return pd.DataFrame(), pd.DataFrame()

    ledger = ledger.copy()
    ledger.columns = [str(c).strip().lower() for c in ledger.columns]
    if not {"date", "ticker", "kind"}.issubset(ledger.columns):
        return pd.DataFrame(), pd.DataFrame()
    for c in ("shares", "split_ratio", "div_per_share", "notes", "price_per_share"):
        if c not in ledger.columns:
            ledger[c] = np.nan
    if "reinvest" not in ledger.columns:
        ledger["reinvest"] = 0
    ledger["date"] = pd.to_datetime(ledger["date"])
    ledger["ticker"] = ledger["ticker"].astype(str).str.upper().str.strip()
    ledger["kind"] = ledger["kind"].astype(str).str.upper().str.strip()
    ledger["reinvest"] = pd.to_numeric(ledger["reinvest"], errors="coerce").fillna(0).astype(int)

    displays: list[pd.DataFrame] = []
    summary_rows: list[dict] = []

    for t in sorted(ledger["ticker"].unique()):
        sub = ledger[ledger["ticker"] == t].sort_values("date").reset_index(drop=True)
        buy_dates = {
            pd.Timestamp(x).normalize()
            for x in sub.loc[sub["kind"] == "BUY", "date"].tolist()
        }
        sh = 0.0
        cum_cash = 0.0
        out_rows: list[dict] = []
        for _, r in sub.iterrows():
            k = r["kind"]
            pr = r.get("price_per_share")
            prf = float(pr) if pd.notna(pr) else None
            usd = np.nan

            if k == "BUY":
                q = float(r["shares"]) if pd.notna(r["shares"]) else 0.0
                sh += q
                if prf is not None:
                    usd = -q * prf
                    act = f"BUY  {q:.6f} @ {prf:.2f}"
                else:
                    act = f"BUY  {q:.6f}"
            elif k == "SELL":
                q = float(r["shares"]) if pd.notna(r["shares"]) else 0.0
                sh -= q
                if prf is not None:
                    usd = q * prf
                    act = f"SELL {q:.6f} @ {prf:.2f}"
                else:
                    act = f"SELL {q:.6f}"
            elif k == "SPLIT":
                ratio = r.get("split_ratio", "")
                m = _split_mult(ratio)
                sh *= m
                usd = 0.0
                rs = str(ratio).strip()
                act = f"SPLIT {rs}" if rs else f"SPLIT {_fmt_split(m)}"
            elif k == "DIV":
                dps = float(r["div_per_share"]) if pd.notna(r.get("div_per_share")) else 0.0
                reinv = int(r.get("reinvest", 0) or 0)
                div_day = pd.Timestamp(r["date"]).normalize()
                # Same-day explicit BUY (typical DRIP) already adds shares; do not also synthetic-reinvest.
                if reinv == 1 and dps > 0 and div_day in buy_dates:
                    usd = 0.0
                    act = f"DIV ${dps:.2f} reinvested (same-day BUY records shares; no duplicate add)"
                elif reinv == 1 and dps > 0 and price_panel is not None:
                    px = _px_on_day(price_panel, t, r["date"])
                    if px and px > 0:
                        cash = sh * dps
                        add = cash / px
                        sh += add
                        usd = 0.0
                        act = f"DIV reinvest ${dps:.4f}/sh → +{add:.6f} sh @ {px:.2f}"
                    else:
                        usd = np.nan
                        act = f"DIV ${dps:.4f}/sh (reinvest; need price_panel Close)"
                else:
                    if dps > 0:
                        usd = sh * dps
                    else:
                        usd = 0.0
                    act = f"DIV ${dps:.4f}/sh (cash)"
            else:
                act = str(k)

            if pd.notna(usd) and np.isfinite(usd):
                cum_cash += float(usd)

            out_rows.append(
                {
                    "date": r["date"],
                    "action": act,
                    "shares_after": sh,
                    "cash_flow_usd": usd,
                    "cash_cumulative_usd": cum_cash,
                }
            )

        ddf = pd.DataFrame(out_rows)
        ddf.insert(0, "ticker", t)
        displays.append(ddf)

        close_today = _last_px(price_panel, t)
        ct = np.nan if close_today is None else float(close_today)
        pos_val = (sh * ct) if pd.notna(ct) else np.nan

        summary_rows.append(
            {
                "ticker": t,
                "shares_now": sh,
                "close_today": ct,
                "position_value_usd": pos_val,
                "net_cash_flow_usd": cum_cash,
                "n_buys": int((sub["kind"] == "BUY").sum()),
                "n_sells": int((sub["kind"] == "SELL").sum()),
                "n_splits": int((sub["kind"] == "SPLIT").sum()),
                "n_divs": int((sub["kind"] == "DIV").sum()),
            }
        )

    hist = pd.concat(displays, ignore_index=True) if displays else pd.DataFrame()
    summ = pd.DataFrame(summary_rows)
    return hist, summ


def hist_summ_pr(
    ledger: pd.DataFrame,
    price_panel: pd.DataFrame | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(history chronology, per-ticker summary). Single internal pass."""
    return _led_run_ix(ledger, price_panel=price_panel)


def sym_hist_tb(ledger: pd.DataFrame, price_panel: pd.DataFrame | None) -> pd.DataFrame:
    """History-by-symbol table only."""
    h, _ = hist_summ_pr(ledger, price_panel)
    return h
