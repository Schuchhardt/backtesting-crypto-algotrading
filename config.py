"""Project configuration."""

import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    dsn: str = os.getenv("DATABASE_URL", "")


def get_db_config() -> DBConfig:
    return DBConfig()
