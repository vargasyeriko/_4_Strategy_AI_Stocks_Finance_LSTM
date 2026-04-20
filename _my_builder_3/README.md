# Builder 3 — growth / defensive portfolio (`src_3`)

Parent suite: `builders/auto.py` → option **3** or `python auto.py 3`.

## Layout

```
_my_builder_3/
├── auto.py              # thin launcher → src_3.run (for future automation)
├── README.md
├── requirements.txt
├── data/                # your_data.pkl — portable `b3_panel_v1` (no PyArrow needed; see data/README.txt)
├── src_3/
│   ├── _0_paths.py      # paths & output dirs
│   ├── _u_entries.py    # user config (buckets, panel name, aliases)
│   ├── _1_fns_io.py     # load panel → close matrix
│   ├── _2_fns_portfolio.py
│   ├── _3_fns_analytics.py
│   ├── _4_fns_charts.py
│   ├── _5_fns_pdf.py
│   └── run.py           # dropdown menu + CLI (this is what you run)
├── _out/                # pie_charts/, equity/ (CSV + PNG), pdf/ — gitignored
├── .mplconfig/          # matplotlib cache (gitignored)
└── notebooks/           # Jupyter + archived ALFA assets — see notebooks/README.md
```

## Run

```bash
cd .../builders/_my_builder_3
pip install -r requirements.txt
python auto.py              # same as: python -m src_3.run
python auto.py summary
python auto.py returns      # growth vs defensive over time: stats + CSV + line chart
```

**Returns over time** (`returns` / menu **5**): equal-weight buy-and-hold inside each bucket, plus a **Blend** using `TARGET_WEIGHT_GROWTH` / `TARGET_WEIGHT_DEFENSIVE` in `_u_entries.py`. The window begins on the first date all names in both buckets have prices (after forward-fill). Writes `_out/equity/bucket_equity_daily.csv` and `equity_growth_vs_defensive.png`.

Configure buckets in `src_3/_u_entries.py`. Menu **4** (PDF) needs `reportlab` (listed in `requirements.txt`).
