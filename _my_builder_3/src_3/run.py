#!/usr/bin/env python3
"""
RULE — execution only. From the folder that contains `src_3/`:  python -m src_3.run

Interactive dropdown menu (and CLI shortcuts). ``auto.py`` only forwards here for future automation.
"""
from __future__ import annotations

import os
import sys

from ._0_paths import BUILDER_ROOT, EQUITY_DIR, ensure_out_dirs
from ._1_fns_io import prepare_close_matrix
from ._2_fns_portfolio import build_bucket_weights, global_target_weights, notionals_at_last
from ._3_fns_analytics import (
    bucket_performance_summary,
    build_bucket_equity_frame,
    describe_universe,
)
from ._u_entries import (
    DEFENSIVE_TICKERS,
    GROWTH_TICKERS,
    PANEL_FILENAME,
    TARGET_WEIGHT_DEFENSIVE,
    TARGET_WEIGHT_GROWTH,
)

_mpl = BUILDER_ROOT / ".mplconfig"
_mpl.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_mpl))


def _print_banner() -> None:
    print()
    print("══════════════════════════════════════════════════════════")
    print("  Builder 3 — Growth / Defensive portfolio (your_data.pkl)")
    print("══════════════════════════════════════════════════════════")


def cmd_summary(close) -> None:
    print(f"\nPanel rows: {len(close)}  |  date range: {close.index.min().date()} → {close.index.max().date()}")
    print(f"Symbols ({len(close.columns)}): {', '.join(map(str, sorted(close.columns)))}")
    g, d = build_bucket_weights(list(close.columns))
    print(f"\nGrowth tickers in panel ({len(g.symbols)}): {g.symbols}")
    print(f"Defensive tickers in panel ({len(d.symbols)}): {d.symbols}")
    tw = global_target_weights(g, d)
    print(f"\nTarget bucket mix: {TARGET_WEIGHT_GROWTH:.0%} growth / {TARGET_WEIGHT_DEFENSIVE:.0%} defensive")
    print("Global target weights (top):")
    for k, v in list(tw.items())[:15]:
        print(f"  {k:8}  {v:.4f}")
    if len(tw) > 15:
        print("  ...")
    n = notionals_at_last(close, tw, capital=100_000.0)
    print("\nNotional $100k at last close (first 10):")
    print(n.head(10).to_string())


def cmd_analytics(close) -> None:
    all_syms = [s for s in GROWTH_TICKERS + DEFENSIVE_TICKERS if s in close.columns]
    tab = describe_universe(close, all_syms)
    print(tab.to_string())


def cmd_export_charts(close) -> None:
    from ._4_fns_charts import save_bucket_pie, save_holdings_pie

    g, d = build_bucket_weights(list(close.columns))
    tw = global_target_weights(g, d)
    ensure_out_dirs()
    p1 = save_bucket_pie(TARGET_WEIGHT_GROWTH, TARGET_WEIGHT_DEFENSIVE)
    print(f"Saved: {p1}")
    if g.weights:
        p2 = save_holdings_pie(g.weights, "Equal-weight within Growth bucket", "pie_holdings_growth.png")
        print(f"Saved: {p2}")
    if d.weights:
        p3 = save_holdings_pie(d.weights, "Equal-weight within Defensive bucket", "pie_holdings_defensive.png")
        print(f"Saved: {p3}")
    p4 = save_holdings_pie(tw, "Global target weights (growth+defensive mix)", "pie_global_target.png")
    print(f"Saved: {p4}")


def cmd_pdf() -> None:
    from ._5_fns_pdf import compile_pie_pdf

    try:
        p = compile_pie_pdf()
        print(f"PDF written: {p}")
    except FileNotFoundError as e:
        print(e, file=sys.stderr)


def cmd_returns_over_time(close) -> None:
    """Growth vs defensive: equal-weight buy-and-hold per bucket, blend, CSV + line chart."""
    from ._4_fns_charts import save_bucket_equity_lines

    g_b, d_b = build_bucket_weights(list(close.columns))
    eqf = build_bucket_equity_frame(
        close,
        g_b.symbols,
        d_b.symbols,
        TARGET_WEIGHT_GROWTH,
        TARGET_WEIGHT_DEFENSIVE,
    )
    if eqf.empty:
        print("Could not build bucket equity curves (need overlapping prices in both buckets).")
        return
    ensure_out_dirs()
    summ = bucket_performance_summary(eqf)
    print("\n=== Growth vs defensive — returns over time (common window) ===\n")
    if not summ.empty:
        for name, row in summ.iterrows():
            print(
                f"  {name:12}  total {row['total_return']:>8.2%}  "
                f"CAGR {row['cagr']:>8.2%}  ann vol {row['ann_vol']:>8.2%}  "
                f"max DD {row['max_drawdown']:>8.2%}"
            )
        print(f"\n  window: {eqf.index[0].date()} → {eqf.index[-1].date()}  ({len(eqf)} trading days)")
    csvp = EQUITY_DIR / "bucket_equity_daily.csv"
    eqf.to_csv(csvp)
    print(f"\nSaved: {csvp}")
    p = save_bucket_equity_lines(eqf)
    print(f"Saved: {p}")


def interactive_menu(close) -> None:
    state = {"close": close}
    while True:
        print(
            """
  1 — Summary (symbols, bucket mix, notionals)
  2 — Per-ticker table (last, vol, total return)
  3 — Pie charts (allocation) → _out/pie_charts/
  4 — Compile PDF from pie PNGs
  5 — Growth vs defensive RETURNS OVER TIME (table + CSV + line chart) → _out/equity/
  6 — Reload panel from disk
  0 — Exit
"""
        )
        choice = input("Choose [0-6]: ").strip()
        if choice == "0":
            print("Bye.")
            return
        c = state["close"]
        if choice == "1":
            cmd_summary(c)
        elif choice == "2":
            cmd_analytics(c)
        elif choice == "3":
            cmd_export_charts(c)
        elif choice == "4":
            cmd_pdf()
        elif choice == "5":
            cmd_returns_over_time(c)
        elif choice == "6":
            state["close"] = prepare_close_matrix(BUILDER_ROOT, PANEL_FILENAME)
            print("Reloaded.")
        else:
            print("Invalid choice.")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    _print_banner()
    close = prepare_close_matrix(BUILDER_ROOT, PANEL_FILENAME)

    if argv:
        head = argv[0].lower()
        if head in ("summary", "s", "1"):
            cmd_summary(close)
        elif head in ("analytics", "a", "2"):
            cmd_analytics(close)
        elif head in ("charts", "c", "3"):
            cmd_export_charts(close)
        elif head in ("pdf", "4"):
            cmd_pdf()
        elif head in ("returns", "r", "5", "equity"):
            cmd_returns_over_time(close)
        else:
            print(
                "Unknown arg. Use: summary | analytics | charts | pdf | returns",
                file=sys.stderr,
            )
            return 1
        return 0

    interactive_menu(close)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
