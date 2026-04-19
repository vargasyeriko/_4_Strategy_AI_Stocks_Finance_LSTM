"""
User inputs for `src_2` — tickers, horizons, paths, training hyperparameters.

From repo root:  python auto.py   (or:  python -m src_2.run — same as root auto)
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAVED_MODELS_DIR = ROOT / "saved_models"
SCALERS_NAME = "scalers_per_ticker.pkl"

# Panel pickle search order (wide OHLCV from fetch — same idea as src_1 `_dta_raw_fetched.pkl`)
_DATA_PKL_CANDIDATES: tuple[Path, ...] = (
    ROOT / "_dta_raw_fetched.pkl",
    ROOT / "_dta_raw_fetched-Copy1.pkl",
    ROOT / "data" / "your_data.pkl",
)


def resolve_data_pkl() -> Path:
    """First existing candidate under `src_2/`."""
    for p in _DATA_PKL_CANDIDATES:
        if p.is_file():
            return p
    raise FileNotFoundError(
        "No panel pickle found in src_2. Place one of:\n  "
        + "\n  ".join(str(p) for p in _DATA_PKL_CANDIDATES)
    )


# Back-compat alias (single resolved path is chosen at runtime)
def data_pkl_path() -> Path:
    return resolve_data_pkl()

# Tickers to offer in menus (must exist in loaded PKL after reshape)
STOCKS: list[str] = [
    "NVDA",
    "TSLA",
    "AMD",
    "AAPL",
    "SOBO",
    "MSFT",
]

# Horizons: trading-day shifts (matches _1_fns_targets column names)
HORIZON_DAYS: dict[str, int] = {
    "3d": 3,
    "7d": 7,
    "30d": 30,
    "90d": 90,
    "180d": 180,
}

TARGET_COLS: list[str] = ["y_3d", "y_7d", "y_30d", "y_90d", "y_180d"]

# Menu: key -> (label, horizon_key)
HORIZON_MENU: list[tuple[str, str, str]] = [
    ("1", "3 days", "3d"),
    ("2", "1 week (7d)", "7d"),
    ("3", "1 month (30d)", "30d"),
    ("4", "3 months (90d)", "90d"),
    ("5", "6 months (180d)", "180d"),
    ("6", "ALL horizons", "all"),
]

# Default fallback if horizon missing from map
TIMESTEPS = 30

# Lookback length per horizon (different signal structure per horizon)
TIMESTEPS_BY_HORIZON: dict[str, int] = {
    "3d": 25,
    "7d": 40,
    "30d": 75,
    "90d": 120,
    "180d": 200,
}

# Training history: short horizons use ~1y; long horizons use ~3y (calendar)
TRAINING_WINDOW_YEARS_SHORT = 1.0
TRAINING_WINDOW_YEARS_LONG = 3.0
SHORT_HORIZONS_FOR_WINDOW: frozenset[str] = frozenset({"3d", "7d", "30d"})

TRAIN_FRAC = 0.8
LSTM_UNITS = 32
DROPOUT_RATE = 0.3
EPOCHS = 50
BATCH_SIZE = 32
EARLY_STOPPING_PATIENCE = 7
RANDOM_SEED = 42

# Minimum rows per ticker (252d vol + sequences + targets; keep headroom)
MIN_ROWS_PER_TICKER = 300

# Target = forward_return / sigma (sigma = vol_60d_raw). Floor avoids blow-ups when vol→0.
MIN_SIGMA_FOR_TARGET = 5e-5
VOL_ANCHOR_COL = "vol_60d_raw"


def timesteps_for_horizon(horizon_key: str) -> int:
    return TIMESTEPS_BY_HORIZON.get(horizon_key, TIMESTEPS)

# Training
VERBOSE_TRAIN = 1
