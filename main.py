"""Main orchestrator for backtesting."""

from datetime import datetime
import json

import pandas as pd

from config import get_db_config
from db.connection import get_connection
from db import queries
from services.market import fetch_ohlcv
from services.runner import load_algorithm
from services.backtest import run_backtest


def main():
    db_cfg = get_db_config()
    conn = get_connection(db_cfg.dsn)

    configs = queries.fetch_algorithm_configs(conn)
    for cfg in configs:
        alg_module = load_algorithm(cfg['slug'])
        algorithm_func = getattr(alg_module, 'run')
        start_date = cfg['start_date']
        if isinstance(start_date, str):
            start_dt = datetime.fromisoformat(start_date)
        else:
            start_dt = start_date
        market_data = fetch_ohlcv(cfg['symbol'], cfg['timeframe'], start_dt)
        close = market_data['close']
        result = run_backtest(close, algorithm_func, cfg['params'])
        queries.save_backtest_result(conn, cfg['id'], result)

    conn.close()


if __name__ == '__main__':
    main()
