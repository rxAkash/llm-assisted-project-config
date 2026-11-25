from datetime import datetime, timedelta

from airflow.decorators import dag, task


@dag(
    schedule="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["ingestion"],
)
def snowflake_to_postgres():
    @task
    def replicate(table: str = "orders") -> int:
        from ingestion.replicate import replicate_table  # heavy import inside task

        return replicate_table(table, key="id", watermark_col="updated_at", last_value="1970-01-01")

    @task.bash
    def dbt_build() -> str:
        return "cd /opt/airflow/dbt && dbt build"

    replicate() >> dbt_build()


snowflake_to_postgres()
