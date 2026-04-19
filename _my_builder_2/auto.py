#!/usr/bin/env python3
# 🚀 SINGLE ENTRY POINT — run everything via ``python auto.py`` (see README.md).

"""
LSTM predictions — single entrypoint for this builder (this file next to ``src_2/``).

  python auto.py                    # menu: train or predict (per-ticker models)
  python auto.py targets            # debug: tail of panel + targets
  python auto.py train              # train only (no menu)

Models are per ticker + horizon: ``src_2/saved_models/NVDA_3d.keras``

Adds this folder (parent of ``src_2/``) to ``sys.path``. Run from ``_my_builder_2/`` or pass the absolute path to ``auto.py``:

  cd .../builders/_my_builder_2 && python auto.py
  python -m src_2.run
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] == "targets":
        from src_2._0_fns_io import load_panel_long
        from src_2._1_fns_targets import add_return_targets
        from src_2._2_fns_features import add_features
        from src_2 import _u_entries as U

        df = load_panel_long()
        df = add_return_targets(df)
        df = add_features(df)
        cols = ["date", "ticker", "close"] + [c for c in U.TARGET_COLS if c in df.columns]
        cols = [c for c in cols if c in df.columns]
        print(df[cols].tail(20).to_string(index=False))
        return
    if argv and argv[0] == "train":
        from src_2._cli import run_train_cli

        run_train_cli()
        return

    from src_2._cli import run_interactive_menu

    run_interactive_menu()


if __name__ == "__main__":
    main()
