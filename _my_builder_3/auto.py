#!/usr/bin/env python3
"""Thin launcher — forwards to ``src_3.run`` (reserved for future automation / scheduling).

Examples:  python auto.py   |   python auto.py returns   |   python auto.py charts
"""
from __future__ import annotations

import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from src_3.run import main

if __name__ == "__main__":
    raise SystemExit(main())
