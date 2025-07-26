# Crypto Algorithm Backtester

Simple framework to run local trading algorithms with historical data.

## Features

- Algorithms live in the `algorithms/` folder. Each exposes a `run(close, params)` function.
- Market data is downloaded from Binance using `ccxt`.
- Backtests are executed with `vectorbt` and results are stored in PostgreSQL.

## Usage

```bash
python main.py
```

Ensure the `DATABASE_URL` environment variable points to your PostgreSQL instance.
