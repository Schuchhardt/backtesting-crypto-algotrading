from datetime import datetime
from typing import Optional

import ccxt
import pandas as pd


def fetch_ohlcv(symbol: str, timeframe: str, start_date: datetime, end_date: Optional[datetime] = None) -> pd.DataFrame:
    """Fetch OHLCV data from Binance."""
    exchange = ccxt.binance()
    since = int(start_date.timestamp() * 1000)
    ohlcv = []
    while True:
        batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
        if not batch:
            break
        ohlcv.extend(batch)
        since = batch[-1][0] + 1
        if end_date and since >= int(end_date.timestamp() * 1000):
            break
        if len(batch) < 1000:
            break
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df
