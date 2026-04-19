"""
One Keras LSTM per (ticker, horizon). Files: saved_models/TICKER_3d.keras
"""
from __future__ import annotations

from pathlib import Path

import tensorflow as tf

from . import _u_entries as U
from ._2_fns_features import FEATURE_COLS, apply_horizon_training_window
from ._3_fns_sequences import build_sequences_for_horizon
from ._9_fns_metrics import eval_arrays

# Reproducibility
tf.keras.utils.set_random_seed(U.RANDOM_SEED)


def _ticker_file_tag(ticker: str) -> str:
    s = str(ticker).strip().upper()
    return "".join(c if c.isalnum() else "_" for c in s)


def model_path(ticker: str, horizon_key: str) -> Path:
    return U.SAVED_MODELS_DIR / f"{_ticker_file_tag(ticker)}_{horizon_key}.keras"


def horizons_missing_for_ticker(ticker: str, keys: list[str]) -> list[str]:
    """Horizon keys with no saved model file for this ticker."""
    return [k for k in keys if not model_path(ticker, k).is_file()]


def count_saved_model_files() -> int:
    """Rough count of .keras files in saved_models/."""
    d = U.SAVED_MODELS_DIR
    if not d.is_dir():
        return 0
    return len(list(d.glob("*.keras")))


def build_lstm(n_features: int, timesteps: int) -> tf.keras.Model:
    """Smaller LSTM for noisy financial series."""
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(timesteps, n_features)),
            tf.keras.layers.LSTM(U.LSTM_UNITS),
            tf.keras.layers.Dropout(U.DROPOUT_RATE),
            tf.keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss="mse")
    return model


def train_horizon(
    df_scaled: "pd.DataFrame",
    horizon_key: str,
    ticker: str,
    epochs: int | None = None,
    batch_size: int | None = None,
) -> tf.keras.Model:
    """Fit on windowed history for this horizon; report MAE + direction accuracy on test split."""
    epochs = epochs if epochs is not None else U.EPOCHS
    batch_size = batch_size if batch_size is not None else U.BATCH_SIZE
    timesteps = U.timesteps_for_horizon(horizon_key)

    n_features = len(FEATURE_COLS)
    t = str(ticker).strip().upper()
    df_t = df_scaled[df_scaled["ticker"] == t].copy()
    if df_t.empty:
        raise ValueError(f"No rows for ticker {ticker!r}")
    df_w = apply_horizon_training_window(df_t, horizon_key)

    X_train, y_train, X_test, y_test, sigma_test = build_sequences_for_horizon(
        df_w,
        horizon_key,
        timesteps=timesteps,
        ticker_filter=t,
    )

    model = build_lstm(n_features, timesteps)
    fit_kw: dict = {
        "epochs": epochs,
        "batch_size": batch_size,
        "verbose": U.VERBOSE_TRAIN,
    }
    if len(X_test) > 0:
        fit_kw["validation_data"] = (X_test, y_test)
        fit_kw["callbacks"] = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=U.EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
            )
        ]

    model.fit(X_train, y_train, **fit_kw)

    if len(X_test) > 0:
        pred_n = model.predict(X_test, verbose=0).ravel()
        pred_ret = pred_n * sigma_test
        y_raw = y_test * sigma_test
        mae, dacc = eval_arrays(y_raw, pred_ret)
        print(
            f"    → test  MAE={mae:.6f}  direction_acc={100.0 * dacc:.1f}%  (50%=random)"
        )

    path = model_path(ticker, horizon_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    model.save(path)
    return model


def _validate_loaded_model(model: tf.keras.Model, horizon_key: str, path: Path) -> None:
    """
    Saved .keras files must match current FEATURE_COLS, timesteps, and LSTM_UNITS.
    Stale files (e.g. after reducing features) cause cryptic MatMul errors at predict time.
    """
    timesteps = U.timesteps_for_horizon(horizon_key)
    n_features = len(FEATURE_COLS)
    inp = model.input_shape
    if inp is not None and len(inp) >= 3:
        _, got_t, got_f = inp[0], inp[1], inp[2]
        if got_t != timesteps or got_f != n_features:
            raise ValueError(
                f"Stale model architecture: {path}\n"
                f"  file expects input (…, {got_t}, {got_f}) but current code uses "
                f"(…, {timesteps}, {n_features}) for horizon {horizon_key!r}.\n"
                f"  Delete saved_models/*_{horizon_key}.keras (or the whole folder) and retrain."
            )
    lstm = next(
        (L for L in model.layers if isinstance(L, tf.keras.layers.LSTM)),
        None,
    )
    if lstm is not None and int(lstm.units) != int(U.LSTM_UNITS):
        raise ValueError(
            f"Stale model architecture: {path}\n"
            f"  LSTM units={lstm.units} but _u_entries.LSTM_UNITS={U.LSTM_UNITS}.\n"
            f"  Delete {path.name} and retrain this horizon."
        )


def load_model(ticker: str, horizon_key: str) -> tf.keras.Model:
    p = model_path(ticker, horizon_key)
    if not p.is_file():
        raise FileNotFoundError(f"Missing trained model: {p}")
    model = tf.keras.models.load_model(p)
    _validate_loaded_model(model, horizon_key, p)
    return model
