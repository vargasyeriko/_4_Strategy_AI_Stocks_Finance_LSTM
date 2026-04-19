"""MAE + directional accuracy (no heavy imports). Renamed from _metrics for naming consistency."""
from __future__ import annotations

import numpy as np


def mean_absolute_error_returns(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(np.asarray(y_pred).ravel() - np.asarray(y_true).ravel())))


def direction_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    yt = np.asarray(y_true).ravel()
    yp = np.asarray(y_pred).ravel()
    return float(np.mean(np.sign(yp) == np.sign(yt)))


def eval_arrays(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    return mean_absolute_error_returns(y_true, y_pred), direction_accuracy(y_true, y_pred)
