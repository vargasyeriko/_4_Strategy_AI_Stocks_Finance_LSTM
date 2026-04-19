# Builder 2 — LSTM strategy pipeline (`src_2`)

Parent suite: `builders/auto.py` routes here as option **2** (or `python auto.py 2` from `builders/`).

```
├── auto.py                     # 🚀 SINGLE ENTRY POINT (run everything)
├── README.md                   # 📘 clean explanation (how to run, what it does)
├── requirements.txt            # 📦 dependencies
├── .gitignore
└── src_2/                      # numbered modules, _u_entries.py, run.py, saved_models/
```

## What it does

Loads a long-format price panel (pickle), builds features and targets, trains or runs per-ticker / per-horizon Keras LSTM models, and prints prediction tables from the interactive menu.

## Setup

```bash
cd /path/to/_my_builder_2
python3 -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
```

Place panel data where `src_2/_u_entries.py` expects it (see `resolve_data_pkl()`). Trained weights go under `src_2/saved_models/`.

## Run

**Canonical (repo root of this builder):**

```bash
python auto.py                 # interactive menu: train / predict
python auto.py train           # train only
python auto.py targets         # debug: tail of panel + targets
```

**Module form:**

```bash
python -m src_2.run
```

## Notebooks

Optional workflows under `src_2/notebooks/` (e.g. exploration); core behavior is via `auto.py`.
