from typing import Callable, Dict, Any

import pandas as pd
import vectorbt as vbt


def run_backtest(close: pd.Series, algorithm_func: Callable[[pd.Series, Dict[str, Any]], Dict[str, pd.Series]], params: Dict[str, Any]):
    """Run a backtest using vectorbt."""
    signals = algorithm_func(close, params)
    entries = signals['entries']
    exits = signals['exits']
    portfolio = vbt.Portfolio.from_signals(close, entries, exits)
    stats = portfolio.stats()
    trades = portfolio.trades.records_readable
    equity = portfolio.value
    return {
        'stats': stats.to_dict(),
        'trades': trades.to_dict('records'),
        'equity': equity.to_list(),
    }
