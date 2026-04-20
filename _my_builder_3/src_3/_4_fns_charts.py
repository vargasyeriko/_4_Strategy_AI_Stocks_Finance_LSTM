"""Matplotlib pie charts for bucket / holdings views."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ._0_paths import EQUITY_DIR, PIE_DIR, ensure_out_dirs


def _palette(n: int) -> list[str]:
    base = [
        "#a11d1d",
        "#d36452",
        "#983912",
        "#1bd1d1",
        "#278fa0",
        "#3070b6",
        "#5858d8",
        "#571688",
        "#a04e94",
        "#32d8a9",
        "#84932a",
        "#ecc046",
    ]
    return [base[i % len(base)] for i in range(n)]


def save_bucket_pie(
    growth_weight: float,
    defensive_weight: float,
    title: str = "Target mix: Growth vs Defensive",
    fname: str = "pie_growth_defensive.png",
) -> Path:
    ensure_out_dirs()
    fig, ax = plt.subplots(figsize=(8, 8))
    sizes = [growth_weight, defensive_weight]
    labels = [f"Growth ({growth_weight:.0%})", f"Defensive ({defensive_weight:.0%})"]
    colors = ["#d36452", "#278fa0"]
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=120,
        colors=colors,
        wedgeprops={"edgecolor": "black", "linewidth": 0.3},
        textprops={"fontsize": 11},
    )
    ax.set_title(title, fontsize=14, fontweight="bold")
    path = PIE_DIR / fname
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def save_holdings_pie(weights: dict[str, float], title: str, fname: str) -> Path:
    ensure_out_dirs()
    w = pd.Series(weights).sort_values(ascending=False)
    if w.sum() <= 0:
        raise ValueError("weights must sum to > 0")
    w = w / w.sum()
    fig, ax = plt.subplots(figsize=(10, 10))
    cols = _palette(len(w))
    ax.pie(
        w.values,
        labels=w.index.tolist(),
        autopct="%1.1f%%",
        colors=cols,
        startangle=120,
        wedgeprops={"edgecolor": "black", "linewidth": 0.2},
        textprops={"fontsize": 9},
    )
    ax.set_title(title, fontsize=13, fontweight="bold")
    path = PIE_DIR / fname
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def save_bucket_equity_lines(
    eq_frame: pd.DataFrame,
    title: str = "Growth vs Defensive — equal-weight within bucket (rebased to $1)",
    fname: str = "equity_growth_vs_defensive.png",
) -> Path:
    """Line chart of normalized equity curves over time."""
    ensure_out_dirs()
    if eq_frame.empty:
        raise ValueError("No equity data to plot")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = {"Growth": "#d36452", "Defensive": "#278fa0", "Blend": "#333333"}
    for col in eq_frame.columns:
        ax.plot(
            eq_frame.index,
            eq_frame[col].values,
            label=col,
            color=colors.get(col, "#666666"),
            linewidth=1.8,
        )
    ax.axhline(1.0, color="#999999", linestyle="--", linewidth=0.8)
    ax.set_ylabel("Portfolio value ($1 at window start)")
    ax.set_xlabel("Date")
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = EQUITY_DIR / fname
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
