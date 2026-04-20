"""Load and normalize the Yahoo-style panel pickle."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from ._u_entries import PANEL_FILENAME, NOISE_TICKERS, TICKER_ALIASES
from ._0_paths import default_panel_path


def _panel_from_portable_v1(blob: dict) -> pd.DataFrame:
    """Rebuild DataFrame from a dict-only pickle (no PyArrow; works on any Python with pandas+numpy)."""
    cols = pd.MultiIndex.from_tuples(tuple(tuple(x) for x in blob["columns"]))
    idx = pd.DatetimeIndex(pd.to_datetime(blob["index_iso"]))
    idx.name = blob.get("index_name")
    return pd.DataFrame(blob["values"], index=idx, columns=cols)


def save_portable_panel_v1(df: pd.DataFrame, path: Path | str) -> None:
    """Write `b3_panel_v1` pickle (float64 values, ISO dates) so `load_panel_pickle` works without PyArrow."""
    p = Path(path)
    idx_iso = [pd.Timestamp(x).strftime("%Y-%m-%d") for x in df.index]
    blob = {
        "fmt": "b3_panel_v1",
        "values": np.ascontiguousarray(np.asarray(df.values), dtype=np.float64),
        "index_iso": idx_iso,
        "index_name": df.index.name,
        "columns": [list(t) for t in df.columns],
    }
    with open(p, "wb") as f:
        pickle.dump(blob, f, protocol=4)


def load_panel_pickle(path: Path | str) -> pd.DataFrame:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Panel pickle not found: {p}")
    with open(p, "rb") as f:
        try:
            raw = pickle.load(f)
        except ModuleNotFoundError as e:
            if getattr(e, "name", "") == "pyarrow":
                raise RuntimeError(
                    "This panel pickle requires PyArrow. Either:\n"
                    "  pip install pyarrow\n"
                    "Or replace data/your_data.pkl with a portable export (dict fmt b3_panel_v1)."
                ) from e
            raise
    if isinstance(raw, dict) and raw.get("fmt") == "b3_panel_v1":
        return _panel_from_portable_v1(raw)
    if isinstance(raw, pd.DataFrame):
        return raw
    raise TypeError(f"Unsupported pickle in {p}: {type(raw).__name__}")


def _drop_noise_multiindex(panel: pd.DataFrame, noise: frozenset[str]) -> pd.DataFrame:
    if not isinstance(panel.columns, pd.MultiIndex):
        return panel[[c for c in panel.columns if c not in noise]]
    lev0 = panel.columns.get_level_values(0)
    mask = ~pd.Series(lev0).isin(noise).values
    return panel.loc[:, mask]


def _rename_level0(panel: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    if not mapping:
        return panel
    if not isinstance(panel.columns, pd.MultiIndex):
        return panel.rename(columns=mapping)
    new_cols = []
    for t in panel.columns:
        L0 = mapping.get(t[0], t[0])
        rest = tuple([L0] + list(t[1:]))
        new_cols.append(rest)
    out = panel.copy()
    out.columns = pd.MultiIndex.from_tuples(new_cols, names=panel.columns.names)
    return out


def _merge_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    if not df.columns.duplicated().any():
        return df
    out: dict[str, pd.Series] = {}
    for c in pd.unique(df.columns):
        block = df.loc[:, df.columns == c]
        out[str(c)] = block.bfill(axis=1).iloc[:, 0]
    return pd.DataFrame(out, index=df.index)


def to_close_wide(panel: pd.DataFrame) -> pd.DataFrame:
    if isinstance(panel.columns, pd.MultiIndex):
        closes = panel.xs("Close", axis=1, level=1).copy()
    else:
        closes = panel.copy()
    closes = closes.sort_index()
    if not pd.api.types.is_datetime64_any_dtype(closes.index):
        closes.index = pd.to_datetime(closes.index)
    return _merge_duplicate_columns(closes)


def prepare_close_matrix(builder_root: Path, filename: str | None = None) -> pd.DataFrame:
    fn = filename or PANEL_FILENAME
    path = default_panel_path(fn, builder_root)
    if not path.is_file():
        raise FileNotFoundError(
            f"Panel not found. Tried: {builder_root / 'data' / fn} and {builder_root / fn}"
        )
    panel = load_panel_pickle(path)
    panel = _drop_noise_multiindex(panel, NOISE_TICKERS)
    panel = _rename_level0(panel, TICKER_ALIASES)
    return to_close_wide(panel)
