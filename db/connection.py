import os
from typing import Optional

import psycopg2


def get_connection(dsn: Optional[str] = None):
    """Return a new database connection using DSN or environment variables."""
    if dsn is None:
        dsn = os.getenv('DATABASE_URL')
    return psycopg2.connect(dsn)
