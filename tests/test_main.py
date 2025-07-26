import sys
import os
import types
from unittest.mock import MagicMock, patch
import pandas as pd

# Provide minimal stub modules for optional dependencies
sys.modules.setdefault('ccxt', types.SimpleNamespace(binance=lambda: None))
psycopg2_stub = types.SimpleNamespace(connect=lambda dsn: MagicMock())
sys.modules.setdefault('psycopg2', psycopg2_stub)
sys.modules.setdefault('vectorbt', types.ModuleType('vectorbt'))

# Ensure project root is on sys.path so `import main` works when tests are run
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import main
from config import DBConfig


def test_main_runs():
    dummy_conn = MagicMock()
    alg_cfg = [{
        'id': 1,
        'slug': 'simple_ma',
        'symbol': 'BTC/USDT',
        'timeframe': '1d',
        'start_date': '2023-01-01',
        'params': {'fast': 1, 'slow': 2},
    }]
    price_data = pd.DataFrame({'close': [1, 2, 3]}, index=pd.date_range('2023-01-01', periods=3))
    backtest_result = {'stats': {}, 'equity': [1, 2, 3], 'trades': []}
    alg_module = types.SimpleNamespace(run=lambda close, params: {'entries': close > 0, 'exits': close < 0})

    with (
        patch.object(main, 'get_db_config', return_value=DBConfig(dsn='')),
        patch.object(main, 'get_connection', return_value=dummy_conn),
        patch.object(main.queries, 'fetch_algorithm_configs', return_value=alg_cfg) as mock_fetch,
        patch.object(main, 'load_algorithm', return_value=alg_module) as mock_load,
        patch.object(main, 'fetch_ohlcv', return_value=price_data) as mock_market,
        patch.object(main, 'run_backtest', return_value=backtest_result) as mock_run,
        patch.object(main.queries, 'save_backtest_result') as mock_save,
    ):
        main.main()
        mock_fetch.assert_called_once_with(dummy_conn)
        mock_load.assert_called_once_with('simple_ma')
        mock_market.assert_called_once()
        mock_run.assert_called_once_with(price_data['close'], alg_module.run, alg_cfg[0]['params'])
        mock_save.assert_called_once_with(dummy_conn, 1, backtest_result)
        dummy_conn.close.assert_called_once()
