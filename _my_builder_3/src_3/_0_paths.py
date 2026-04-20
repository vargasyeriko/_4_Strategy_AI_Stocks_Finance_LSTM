"""Filesystem layout — single place for path resolution."""
from __future__ import annotations

from pathlib import Path

# Parent of `src_3/` — builder root (auto.py, data/, src_3/, notebooks/, _out/)
BUILDER_ROOT: Path = Path(__file__).resolve().parents[1]

DATA_DIR: Path = BUILDER_ROOT / "data"
NOTEBOOKS_DIR: Path = BUILDER_ROOT / "notebooks"

OUT_DIR: Path = BUILDER_ROOT / "_out"
PIE_DIR: Path = OUT_DIR / "pie_charts"
PDF_DIR: Path = PIE_DIR / "pdf"
EQUITY_DIR: Path = OUT_DIR / "equity"


def default_panel_path(filename: str, builder_root: Path | None = None) -> Path:
    """Preferred: ``<builder>/data/<filename>``; falls back to builder root."""
    root = builder_root if builder_root is not None else BUILDER_ROOT
    primary = root / "data" / filename
    if primary.is_file():
        return primary
    fallback = root / filename
    if fallback.is_file():
        return fallback
    return primary


def ensure_out_dirs() -> None:
    PIE_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    EQUITY_DIR.mkdir(parents=True, exist_ok=True)
