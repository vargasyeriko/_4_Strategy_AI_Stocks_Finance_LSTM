"""
Interactive CLI: predict (stock numbers + horizons) and train.

Set TF_CPP_MIN_LOG_LEVEL before importing TensorFlow (via _4).
"""
from __future__ import annotations

import os
import re
import sys

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

from . import _u_entries as U
from ._0_fns_io import load_panel_long
from ._1_fns_targets import add_return_targets
from ._2_fns_features import add_features, prepare_ml_frame, save_scalers, tickers_eligible_for_ml
from ._4_fns_models import (
    count_saved_model_files,
    horizons_missing_for_ticker,
    train_horizon,
)
from ._u_entries import resolve_data_pkl
from ._5_fns_predict import (
    collect_predictions_table,
    print_predictions_table_colored,
    suppress_tensorflow_predict_noise,
)


def _menu_tickers() -> list[str]:
    """Only names that pass targets+features+row counts (same bar as training)."""
    return tickers_eligible_for_ml()


def _horizon_keys_from_menu(sel: str) -> list[str]:
    for key, _label, hid in U.HORIZON_MENU:
        if sel == key:
            if hid == "all":
                return list(U.HORIZON_DAYS.keys())
            return [hid]
    return []


def _parse_stock_indices(line: str, n_stocks: int) -> list[int]:
    """Parse '1,3,5' / '1 2 3' / '1-3' into 1-based indices (deduped, ordered)."""
    raw = line.strip()
    if not raw:
        return []
    parts: list[str] = []
    for chunk in re.split(r"[\s,;]+", raw):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk and chunk.count("-") == 1:
            a, b = chunk.split("-", 1)
            try:
                lo, hi = int(a.strip()), int(b.strip())
                for k in range(lo, hi + 1):
                    parts.append(str(k))
            except ValueError:
                parts.append(chunk)
        else:
            parts.append(chunk)

    seen: set[int] = set()
    out: list[int] = []
    for p in parts:
        try:
            i = int(p)
        except ValueError:
            continue
        if 1 <= i <= n_stocks and i not in seen:
            seen.add(i)
            out.append(i)
    return out


def _print_saved_models_status() -> None:
    n = count_saved_model_files()
    if n == 0:
        print("Saved models: none (.keras files are per ticker + horizon, e.g. NVDA_3d.keras).")
    else:
        print(f"Saved models: {n} file(s) under {U.SAVED_MODELS_DIR}/")


def run_interactive_menu() -> None:
    """Default `python auto.py`: data path, model status, train or predict."""
    try:
        src = resolve_data_pkl()
    except FileNotFoundError as e:
        print(e)
        return

    print()
    print("════════════════════════════════════════")
    print("  LSTM — per-ticker models")
    print("════════════════════════════════════════")
    print(f"  Data: {src}")
    print()
    _print_saved_models_status()
    print()
    print("  1 — Train (every ticker in fetch × horizons you choose)")
    print("  2 — Predict (colored table; models per ticker you pick)")
    print("  0 — Exit")
    print()

    choice = input("Choose [1/2/0]: ").strip()
    if choice == "0":
        print("Bye.")
        return
    if choice == "1":
        run_train_cli()
        _print_saved_models_status()
        yn = input("\nRun predictions now? [y/N]: ").strip().lower()
        if yn in ("y", "yes"):
            run_predict_cli()
        return
    if choice == "2":
        run_predict_cli()
        return
    print("Invalid choice.")


def run_predict_cli() -> None:
    """Ask for stock numbers + horizon; print prediction tables only."""
    try:
        src = resolve_data_pkl()
    except FileNotFoundError as e:
        print(e)
        return

    print(f"\nData file: {src}")

    tickers = _menu_tickers()
    if not tickers:
        print(
            "No tickers pass feature + history filters (MIN_ROWS_PER_TICKER). "
            "Check your PKL or lower MIN_ROWS_PER_TICKER in _u_entries.py."
        )
        return

    print()
    print("Stocks you can predict (number → ticker). * = in _u_entries.STOCKS")
    for i, t in enumerate(tickers, start=1):
        mark = "*" if t in U.STOCKS else " "
        print(f"  {i:>3} {mark} {t}")

    print()
    line = input("Stock numbers to predict (e.g. 1,3 5 or 1-3): ").strip()
    idxs = _parse_stock_indices(line, len(tickers))
    if not idxs:
        print("No valid selection.")
        return

    selected = [str(tickers[i - 1]).strip().upper() for i in idxs]
    print()
    for key, lab, _hid in U.HORIZON_MENU:
        print(f"  {key} → {lab}")
    hsel = input("Horizon (1-6): ").strip()
    keys = _horizon_keys_from_menu(hsel)
    if not keys:
        print("Invalid horizon.")
        return

    ready: list[str] = []
    for sym in selected:
        miss = horizons_missing_for_ticker(sym, keys)
        if miss:
            print(
                f"\n{sym}: missing model(s): {', '.join(miss)} "
                f"(e.g. {U.SAVED_MODELS_DIR}/{sym}_{miss[0]}.keras)"
            )
            print("  Train: python auto.py → 1 → pick the same horizon(s).")
        else:
            ready.append(sym)

    if not ready:
        return

    suppress_tensorflow_predict_noise()
    print("\nLoading data & models…")
    df_scaled, _, _ = prepare_ml_frame(ticker_allowlist=ready)

    try:
        combined, stale_skips = collect_predictions_table(df_scaled, ready, keys)
    except Exception as e:
        print(f"Prediction error: {e}")
        return

    print()
    print_predictions_table_colored(combined)
    if stale_skips:
        print("Skipped (model file does not match current code — retrain that horizon):")
        seen: set[str] = set()
        for line in stale_skips:
            if line not in seen:
                seen.add(line)
                print(f"  • {line}")
        print()


def run_train_cli() -> None:
    """Train per (ticker, horizon) for every eligible ticker in the fetched PKL."""
    try:
        print(f"Data file: {resolve_data_pkl()}\n")
    except FileNotFoundError as e:
        print(e)
        return

    print("Loading — ALL symbols that pass feature/history filters…")
    df_scaled, scaler, _ = prepare_ml_frame(ticker_allowlist=None)
    syms = sorted(df_scaled["ticker"].astype(str).str.upper().unique())
    print(f"  → {len(syms)} tickers, {len(df_scaled):,} rows.")
    save_scalers(scaler)
    print(f"Saved scalers → {U.SAVED_MODELS_DIR / U.SCALERS_NAME}")
    print()
    for key, lab, _hid in U.HORIZON_MENU:
        print(f"  {key} → {lab}")
    hsel = input("Horizon to train (1-6): ").strip()
    keys = _horizon_keys_from_menu(hsel)
    if not keys:
        print("Invalid horizon.")
        return

    total = len(syms) * len(keys)
    done = 0
    for t in syms:
        for k in keys:
            done += 1
            print(f"--- [{done}/{total}] {t} / {k} ---")
            try:
                train_horizon(df_scaled, k, ticker=t)
            except ValueError as e:
                print(f"  skip {t} {k}: {e}")
            except Exception as e:
                print(f"  skip {t} {k}: {e}")
    print("Done.")


def main() -> None:
    av = sys.argv[1:]
    if av and av[0] == "targets":
        df = load_panel_long()
        df = add_return_targets(df)
        df = add_features(df)
        cols = ["date", "ticker", "close"] + [c for c in U.TARGET_COLS if c in df.columns]
        cols = [c for c in cols if c in df.columns]
        print(df[cols].tail(20).to_string(index=False))
        return
    if av and av[0] == "train":
        run_train_cli()
        return
    run_interactive_menu()


if __name__ == "__main__":
    main()
