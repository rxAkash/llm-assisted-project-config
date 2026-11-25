"""Incremental Snowflake -> Postgres replication using a watermark column."""
import logging
from collections.abc import Iterable, Sequence
from typing import Any

import psycopg
import snowflake.connector

from ingestion.config import Settings

log = logging.getLogger(__name__)


def build_extract_sql(table: str, watermark_col: str) -> str:
    # table/column names come from trusted config, values are bound parameters
    return f"SELECT * FROM {table} WHERE {watermark_col} > %s ORDER BY {watermark_col}"  # noqa: S608


def upsert_sql(table: str, columns: Sequence[str], key: str) -> str:
    cols = ", ".join(columns)
    params = ", ".join(["%s"] * len(columns))
    updates = ", ".join(f"{c}=EXCLUDED.{c}" for c in columns if c != key)
    return (
        f"INSERT INTO {table} ({cols}) VALUES ({params}) "  # noqa: S608
        f"ON CONFLICT ({key}) DO UPDATE SET {updates}"
    )


def replicate_table(table: str, key: str, watermark_col: str, last_value: Any) -> int:
    s = Settings()
    sf = snowflake.connector.connect(
        account=s.snowflake_account,
        user=s.snowflake_user,
        password=s.snowflake_password,
        warehouse=s.snowflake_warehouse,
        database=s.snowflake_database,
    )
    total = 0
    with sf.cursor() as cur, psycopg.connect(s.postgres_dsn) as pg:
        cur.execute(
            build_extract_sql(table, watermark_col).replace("%s", "%(wm)s"), {"wm": last_value}
        )
        columns = [d[0].lower() for d in cur.description]
        sql = upsert_sql(table, columns, key)
        while rows := cur.fetchmany(5000):
            _write(pg, sql, rows)
            total += len(rows)
        pg.commit()
    log.info("replicated %s rows into %s", total, table)
    return total


def _write(pg: psycopg.Connection[Any], sql: str, rows: Iterable[Sequence[Any]]) -> None:
    with pg.cursor() as c:
        c.executemany(sql, rows)
