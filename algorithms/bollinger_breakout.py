import pandas as pd


def run(close: pd.Series, params: dict) -> dict:
    """Bollinger Bands breakout strategy.

    Parameters
    ----------
    close : pd.Series
        Close price series.
    params : dict
        Dictionary with 'period' and 'std_multiplier'.
    """
    period = params.get('period', 20)
    std_mult = params.get('std_multiplier', 2)

    ma = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = ma + std_mult * std
    lower = ma - std_mult * std

    entries = close > upper
    exits = close < lower

    return {'entries': entries, 'exits': exits}
