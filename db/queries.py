from typing import Any, Dict, List

import pandas as pd


def fetch_algorithm_configs(conn) -> List[Dict[str, Any]]:
    """Retrieve algorithm configurations from the database."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, slug, symbol, timeframe, start_date, params FROM algorithms WHERE active = true")
        rows = cur.fetchall()
    configs = []
    for row in rows:
        config = {
            'id': row[0],
            'slug': row[1],
            'symbol': row[2],
            'timeframe': row[3],
            'start_date': row[4],
            'params': row[5],
        }
        configs.append(config)
    return configs


def save_backtest_result(conn, algorithm_id: int, result: Dict[str, Any]):
    """Store backtest result in the database."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO algorithm_tests (algorithm_id, stats, equity, trades)
            VALUES (%s, %s, %s, %s)
            """,
            (
                algorithm_id,
                result['stats'],
                result['equity'],
                result['trades'],
            ),
        )
    conn.commit()
