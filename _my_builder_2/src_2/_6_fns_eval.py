"""
Test-set metrics; optional MAE helper that loads a saved model.
"""
from __future__ import annotations

from . import _u_entries as U
from ._3_fns_sequences import build_sequences_for_horizon
from ._4_fns_models import load_model
from ._9_fns_metrics import direction_accuracy, eval_arrays, mean_absolute_error_returns


def mae_test(df_scaled, ticker: str, horizon_key: str) -> float | None:
    """Mean absolute error on time-based test sequences for one ticker."""
    ts = U.timesteps_for_horizon(horizon_key)
    _, _, X_test, y_test_n, sigma_test = build_sequences_for_horizon(
        df_scaled,
        horizon_key,
        timesteps=ts,
        ticker_filter=str(ticker).strip().upper(),
    )
    if len(X_test) == 0:
        return None
    model = load_model(ticker, horizon_key)
    pred_n = model.predict(X_test, verbose=0).ravel()
    pred_ret = pred_n * sigma_test
    y_raw = y_test_n * sigma_test
    return mean_absolute_error_returns(y_raw, pred_ret)
