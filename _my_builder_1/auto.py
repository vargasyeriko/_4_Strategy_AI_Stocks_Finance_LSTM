#!/usr/bin/env python3
# 🚀 SINGLE ENTRY POINT — run everything via ``python auto.py`` (see README.md).

"""
One-shot runner for the `src_1` pipeline (same as `python -m src_1.run`).

Run from anywhere:

    python /path/to/_my_builder_1/auto.py

Notebooks call the same file with ``runpy.run_path(..., run_name="src1_notebook_bootstrap")``
so ``sys.path`` is fixed but ``if __name__ == "__main__"`` does not run ``main()``.
"""
from __future__ import annotations

import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from src_1.run import main

if __name__ == "__main__":
    main()
