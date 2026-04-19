"""
CORE SYSTEM — `src_1`

- `entries`              `FETCH_STOCKS`, `MY_STOCKS`
- `_0_fns_get_data`      `sync_raw_pkl`, `default_raw_pkl_path` — **only** writes `_dta_raw_fetched.pkl` (incremental; path is next to these modules, not cwd)
- `_1_fns_history_by_symbol`  `stk_ledg_df`, `hist_summ_pr`, `sym_hist_tb`
- `_2_gainloss`          `entry_gl_tb`
- `_3_summary`           `portf_sum_tb`
- `run`                  `python -m src_1.run` (cwd = parent of `src_1/`)
- Notebooks              `_RUN_.ipynb` (under `builders/_my_builder_1/`)
"""
