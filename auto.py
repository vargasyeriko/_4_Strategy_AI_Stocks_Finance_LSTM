#!/usr/bin/env python3
# 🚀 SINGLE ENTRY POINT — run everything via ``python auto.py`` (see README.md).

"""
Master launcher: routes to Builder 1–3.

  python auto.py              # interactive menu
  python auto.py 1            # Builder 1 — portfolio / ledger (src_1)
  python auto.py 2            # Builder 2 — LSTM (src_2)
  python auto.py 3            # Builder 3 — growth/defensive on your_data.pkl (src_3)
  python auto.py 2 train      # forward args to Builder 2 auto.py
  python auto.py portfolio    # alias for 1
  python auto.py lstm         # alias for 2
  python auto.py alfa         # alias for 3
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_B1 = _ROOT / "_my_builder_1" / "auto.py"
_B2 = _ROOT / "_my_builder_2" / "auto.py"
_B3 = _ROOT / "_my_builder_3" / "auto.py"

_ALIASES_1 = frozenset({"1", "b1", "portfolio", "ledger", "src1"})
_ALIASES_2 = frozenset({"2", "b2", "lstm", "strategy", "src2"})
_ALIASES_3 = frozenset({"3", "b3", "alfa", "growth", "src3"})


def _run_builder(script: Path, forwarded: list[str]) -> int:
    import subprocess

    if not script.is_file():
        print(f"Missing: {script}", file=sys.stderr)
        return 2
    env = os.environ.copy()
    # Keep cwd as suite root so relative paths in docs still make sense
    r = subprocess.run([sys.executable, str(script)] + forwarded, cwd=_ROOT)
    return int(r.returncode)


def _menu() -> int:
    print()
    print("════════════════════════════════════════")
    print("  Strategy builders")
    print("════════════════════════════════════════")
    print("  1 — Portfolio / ledger        (_my_builder_1 / src_1)")
    print("  2 — LSTM predictions           (_my_builder_2 / src_2)")
    print("  3 — Growth / defensive (panel) (_my_builder_3 / src_3)")
    print("  0 — Exit")
    print()
    choice = input("Choose [1/2/3/0]: ").strip()
    if choice == "0":
        print("Bye.")
        return 0
    if choice == "1":
        return _run_builder(_B1, [])
    if choice == "2":
        return _run_builder(_B2, [])
    if choice == "3":
        return _run_builder(_B3, [])
    print("Invalid choice.")
    return 1


def main() -> int:
    av = sys.argv[1:]
    if not av:
        return _menu()

    head = av[0].lower()
    rest = av[1:]

    if head in _ALIASES_1:
        return _run_builder(_B1, rest)
    if head in _ALIASES_2:
        return _run_builder(_B2, rest)
    if head in _ALIASES_3:
        return _run_builder(_B3, rest)

    print("Unknown command. Examples:", file=sys.stderr)
    print("  python auto.py           # menu", file=sys.stderr)
    print("  python auto.py 1         # Builder 1", file=sys.stderr)
    print("  python auto.py 2 train   # Builder 2, train mode", file=sys.stderr)
    print("  python auto.py 3 summary # Builder 3, one-shot", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
