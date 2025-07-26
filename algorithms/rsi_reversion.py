import pandas as pd


def run(close: pd.Series, params: dict) -> dict:
    """RSI mean reversion strategy.

    Parameters
    ----------
    close : pd.Series
        Series of close prices.
    params : dict
        Should contain 'rsi_period', 'oversold', and 'overbought'.

    Returns
    -------
    dict
        Contains 'entries' and 'exits' boolean Series.
    """
    period = params.get('rsi_period', 14)
    oversold = params.get('oversold', 30)
    overbought = params.get('overbought', 70)

    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(period).mean()
    roll_down = down.rolling(period).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))

    entries = rsi < oversold
    exits = rsi > overbought

    return {'entries': entries, 'exits': exits}
