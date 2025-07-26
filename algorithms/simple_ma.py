import pandas as pd


def run(close: pd.Series, params: dict) -> dict:
    """Simple moving average crossover strategy.

    Parameters
    ----------
    close : pd.Series
        Series of close prices.
    params : dict
        Dictionary with keys `fast` and `slow` for periods.

    Returns
    -------
    dict
        Contains 'entries' and 'exits' boolean Series.
    """
    fast_period = params.get('fast', 10)
    slow_period = params.get('slow', 20)

    fast_ma = close.rolling(fast_period).mean()
    slow_ma = close.rolling(slow_period).mean()

    entries = fast_ma > slow_ma
    exits = fast_ma < slow_ma

    return {'entries': entries, 'exits': exits}
