"""
All user input for `src_1`:

- **FETCH_STOCKS** — symbols to download from Yahoo (OHLCV panel). Can include watchlist
  tickers beyond `MY_STOCKS`.
- **MY_STOCKS** — positions you track: each symbol → list of trade rows (buy/sell/split/div).
"""
from __future__ import annotations

stocks_all  = [
    "AAPL",
    "TREE",
    "NVDA",   # Nvidia :contentReference[oaicite:0]{index=0}
    "AMD",    # AMD :contentReference[oaicite:1]{index=1}
    "SOXX",   # iShares Semiconductor ETF
    "CRSP",   # CRISPR Therapeutics
    "TSLA",   # Tesla
    "ROKU",   # Roku
    "TSM",    # Taiwan Semiconductor
    "SSNLF",  # Samsung Electronics (OTC US listing)
    "ASML",   # ASML
    "AVGO",   # Broadcom
    "COIN",   # Coinbase
    "HOOD",   # Robinhood :contentReference[oaicite:2]{index=2}
    "PLTR",   # Palantir :contentReference[oaicite:3]{index=3}
    "ACHR",   # Archer Aviation
    "SHOP",   # Shopify
    "SOBO",   # South Bow Corporation
    "RBLX",   # Roblox
]
# Yahoo panel: which tickers to fetch (edit freely)
FETCH_STOCKS: list[str] = stocks_all 

# Your holdings / trades: type = buy | sell | split | dividend
MY_STOCKS: dict[str, list[dict]] = {
    "NFLX": [
        {"type": "buy", "date": "2022-04-19", "shares": 2.142813, "price_per_share": 245.00},
        {"type": "buy", "date": "2022-05-01", "shares": 2.608105, "price_per_share": 191.71},
        {"type": "buy", "date": "2022-05-05", "shares": 2.491156, "price_per_share": 200.71},
        {"type": "buy", "date": "2022-06-10", "shares": 0.544918, "price_per_share": 183.51},
        {"type": "sell", "date": "2022-06-14", "shares": 4.672151, "price_per_share": 169.79},
        {"type": "split", "date": "2025-11-17", "description": "10:1 forward split"},
        {"type": "sell", "date": "2026-03-24", "shares": 3.0, "price_per_share": 92.77},
    ],
    "NVDA": [
        {"type": "buy", "date": "2022-04-21", "shares": 1.378993, "price_per_share": 217.55, "total": -300.00},
        {"type": "buy", "date": "2022-06-11", "shares": 1.18925, "price_per_share": 159.76, "total": -189.99},
        {"type": "sell", "date": "2022-06-14", "shares": 2.054594, "price_per_share": 157.33, "total": 323.25},
        {"type": "dividend", "date": "2022-07-01", "amount": 0.06, "reinvested": False},
        {"type": "dividend", "date": "2022-09-29", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2022-12-22", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2023-03-29", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2023-06-30", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2023-09-28", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2023-12-28", "amount": 0.02, "reinvested": False},
        {"type": "dividend", "date": "2024-03-27", "amount": 0.02, "reinvested": False},
        {"type": "split", "date": "2024-06-10", "description": "10:1 forward split"},
        {"type": "dividend", "date": "2024-06-28", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2024-10-03", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2024-12-27", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2025-04-02", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2025-07-03", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2025-10-02", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2025-12-26", "amount": 0.05, "reinvested": True},
        {"type": "dividend", "date": "2026-04-01", "amount": 0.05, "reinvested": True},
    ],
    "AAPL": [

        # -------------------------
        # 2022 (pre + exit)
        # -------------------------
        {"type": "buy",  "date": "2022-05-16", "shares": 3.445187, "price_per_share": 145.13},
        {"type": "buy",  "date": "2022-05-18", "shares": 1.404613, "price_per_share": 142.39},
        {"type": "buy",  "date": "2022-06-07", "shares": 1.685203, "price_per_share": 148.35},
        {"type": "sell", "date": "2022-06-14", "shares": 2.61396,  "price_per_share": 133.00},

        # -------------------------
        # Dividends (no shares info → cash only)
        # -------------------------
        {"type": "dividend", "date": "2022-08-11", "amount": 0.90, "reinvested": False},
        {"type": "dividend", "date": "2022-11-10", "amount": 0.90, "reinvested": False},

        {"type": "dividend", "date": "2023-02-16", "amount": 0.90, "reinvested": False},
        {"type": "dividend", "date": "2023-05-18", "amount": 0.94, "reinvested": False},
        {"type": "dividend", "date": "2023-08-17", "amount": 0.94, "reinvested": False},
        {"type": "dividend", "date": "2023-11-16", "amount": 0.94, "reinvested": False},

        {"type": "dividend", "date": "2024-02-15", "amount": 0.94, "reinvested": False},

        # -------------------------
        # DRIP phase — only `buy` rows here. (Do not also add `dividend`+reinvested for the
        # same date: `_led_run_ix` would add shares twice — once from this buy, once from
        # synthetic reinvest = sh * div_per_share / price.)
        # -------------------------
        {"type": "buy", "date": "2024-05-16", "shares": 0.005151, "price_per_share": 190.22},
        {"type": "buy", "date": "2024-08-15", "shares": 0.004365, "price_per_share": 224.47},
        {"type": "buy", "date": "2024-11-14", "shares": 0.004362, "price_per_share": 224.62},
        {"type": "buy", "date": "2025-02-13", "shares": 0.004015, "price_per_share": 244.06},
        {"type": "buy", "date": "2025-05-15", "shares": 0.004848, "price_per_share": 210.38},
        {"type": "buy", "date": "2025-08-14", "shares": 0.004431, "price_per_share": 232.45},
        {"type": "buy", "date": "2025-11-13", "shares": 0.003779, "price_per_share": 272.49},
        {"type": "buy", "date": "2026-02-12", "shares": 0.003965, "price_per_share": 259.75},

        {"type": "sell", "date": "2026-03-24", "shares": 2.0, "price_per_share": 254.47},
    ],
    "TREE": [
        {"type": "buy", "date": "2022-05-04", "shares": 2.558257, "price_per_share": 78.18},
        {"type": "sell", "date": "2022-06-14", "shares": 1.53, "price_per_share": 54.99},
    ],
    "AMD": [
        {"type": "buy", "date": "2026-04-16", "shares": 0.46, "price_per_share": 273.69},
    ],
    "ASML": [
        {"type": "buy", "date": "2026-04-16", "shares": 0.039, "price_per_share": 1417.28},
    ],
    "AVGO": [
        {"type": "buy", "date": "2026-04-16", "shares": 0.056, "price_per_share": 397.16},
    ],
    # SOBO: DRIP buys + matching reinvested dividends (same day). Ledger skips duplicate share add on DIV
    # when a BUY exists that date — see `_led_run_ix` in `_1_fns_history_by_symbol.py`.
    "SOBO": [
        {"type": "buy", "date": "2025-01-31", "shares": 0.004645, "price_per_share": 23.68},
        {"type": "dividend", "date": "2025-01-31", "amount": 0.11, "reinvested": True},
        {"type": "buy", "date": "2025-04-15", "shares": 0.004863, "price_per_share": 24.67},
        {"type": "dividend", "date": "2025-04-15", "amount": 0.12, "reinvested": True},
        {"type": "buy", "date": "2025-07-15", "shares": 0.004506, "price_per_share": 26.63},
        {"type": "dividend", "date": "2025-07-15", "amount": 0.12, "reinvested": True},
        {"type": "buy", "date": "2025-10-15", "shares": 0.004468, "price_per_share": 26.86},
        {"type": "dividend", "date": "2025-10-15", "amount": 0.12, "reinvested": True},
        {"type": "buy", "date": "2026-01-15", "shares": 0.004507, "price_per_share": 26.62},
        {"type": "dividend", "date": "2026-01-15", "amount": 0.12, "reinvested": True},
        {"type": "buy", "date": "2026-04-15", "shares": 0.003685, "price_per_share": 32.56},
        {"type": "dividend", "date": "2026-04-15", "amount": 0.12, "reinvested": True},
    ],
}
