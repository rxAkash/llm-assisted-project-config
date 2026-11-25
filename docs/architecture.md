# Architecture
Snowflake (source) -> `ingestion` (incremental upsert) -> Postgres -> `api` (FastAPI).
dbt builds marts in Snowflake; Airflow orchestrates ingestion then dbt. Terraform provisions AWS (RDS, networking).
