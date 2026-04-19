# Builder 1 — portfolio / ledger pipeline (`src_1`)

Parent suite: `builders/auto.py` routes here as option **1** (or `python auto.py 1` from `builders/`).

```
├── auto.py                     # 🚀 SINGLE ENTRY POINT (run everything)
├── README.md                   # 📘 clean explanation (how to run, what it does)
├── requirements.txt            # 📦 dependencies
├── .gitignore
└── src_1/                      # numbered modules + entries.py + run.py
```

## What it does

Loads synced panel data, joins ledger history, prints gain/loss tables and per-ticker summaries (see `src_1/run.py`).

## Setup

```bash
cd /path/to/_my_builder_1
python3 -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
```

## Run

From this folder (or pass the absolute path to `auto.py`):

```bash
python auto.py
```

Same behavior:

```bash
python -m src_1.run
```

## Notebooks

`_RUN_.ipynb` and `_check_.ipynb` live next to `auto.py`; they can bootstrap `sys.path` and call into `src_1` without duplicating logic.
