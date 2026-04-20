"""
RULE 3 — execution only. From the folder that contains `src_1/`:  python -m src_1.run
"""
from __future__ import annotations

from ._0_fns_get_data import sync_raw_pkl
from ._1_fns_history_by_symbol import hist_summ_pr, stk_ledg_df
from ._2_gainloss import entry_gl_tb
from ._3_summary import earn_summ_tb, portf_sum_tb


def main() -> None:
    _, df_px = sync_raw_pkl(verbose=True)

    raw = stk_ledg_df()
    hist, summ = hist_summ_pr(raw, df_px)

    gain = entry_gl_tb(hist, df_px)
    final = portf_sum_tb(summ)
    earn = earn_summ_tb(final)

    print("=== Table: Ledger history by symbol ===")
    if hist.empty:
        print("(no trades)")
    else:
        print(hist.to_string(index=False))
    print()
    print("=== Table: % gain/loss per entry (split-adjusted entry vs close) ===")
    if gain.empty:
        print("(no BUY rows / no price)")
    else:
        print(gain.to_string(index=False))
    print()
    print("=== Table: Per ticker — shares, last close, est. value, net ledger cash flow ===")
    if final.empty:
        print("(no summary)")
    else:
        print(final.to_string(index=False))
    print()
    print("=== Table: Portfolio summary (totals and earnings vs ledger) ===")
    if earn.empty:
        print("(no portfolio summary)")
    else:
        print(earn.to_string(index=False))


if __name__ == "__main__":
    main()
