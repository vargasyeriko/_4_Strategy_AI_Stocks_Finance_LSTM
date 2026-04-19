# Strategy builders — unified folder

```
builders/
├── auto.py                     # 🚀 SINGLE ENTRY POINT (run everything)
├── README.md                   # 📘 clean explanation (how to run, what it does)
├── requirements.txt            # 📦 dependencies
├── .gitignore
├── _my_builder_1/              # Portfolio / ledger pipeline (src_1)
│   ├── auto.py
│   ├── README.md
│   ├── requirements.txt
│   └── src_1/
└── _my_builder_2/              # LSTM strategy pipeline (src_2)
    ├── auto.py
    ├── README.md
    ├── requirements.txt
    ├── src_2/
    └── …
```

## Quick start

```bash
cd /path/to/a4yy_STRATEGY/builders
python3 -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
python auto.py
```

You get a menu: **1** = Builder 1 (sync panel + ledger tables), **2** = Builder 2 (train / predict LSTMs).

## Direct routing (no menu)

| Command | Effect |
|--------|--------|
| `python auto.py 1` | Runs `_my_builder_1/auto.py` |
| `python auto.py 2` | Runs `_my_builder_2/auto.py` (interactive menu inside) |
| `python auto.py 2 train` | Forwards `train` to Builder 2 |
| `python auto.py portfolio` | Same as `1` |
| `python auto.py lstm` | Same as `2` |

Each sub-builder keeps its own `README.md` and optional venv; the master `requirements.txt` here is a **union** of both stacks so one install covers the suite.

## Layout note

This folder used to live as two siblings `_my_builder_1` and `_my_builder_2` at the repo root; they are now nested here under **`builders/`** with this master entrypoint.
