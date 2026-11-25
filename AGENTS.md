# LLM Assisted Project (sample monorepo)
Snowflake -> Postgres replication, dbt transformations, Airflow orchestration, FastAPI serving layer.

## Commands
- Setup: `make setup` (uv venv + pre-commit; creates `.env` from `.env.example`)   - Test all: `make test`
- Lint/format: `make lint` / `make fmt`   - Types: `make typecheck`   - All checks: `make check`
- Run Python tools via `uv run <tool>` (never bare `pytest`/`ruff`/`mypy`)
- Local stack: `make up` / `make down`
- dbt: `make dbt-build`        - Terraform plan: `make tf-plan ENV=dev`

## Layout
- `ingestion/`  Python package: Snowflake -> Postgres incremental replication
- `dbt/`        staging -> marts models, tests, sources
- `airflow/dags/` DAGs only orchestrate; business logic lives in `ingestion/` or `dbt/`
- `api/`        FastAPI service reading from Postgres
- `terraform/`  modules + envs (dev/prod). Never run `apply` locally.
- `docs/adr/`   Architecture decisions; read before changing design

## Conventions
- Python 3.11, type hints required, Ruff + mypy clean, pytest for tests
- SQL: lowercase, CTEs over subqueries, sqlfluff clean; every dbt model has a yml with tests
- DAGs: idempotent tasks, no top-level heavy imports, `catchup=False` unless justified
- Logging via `logging` (no print). Config via env vars (pydantic-settings).

## Hard rules
- NEVER commit secrets or read `.env`; use `.env.example` for new variables
- NEVER run `terraform apply`/`destroy`, `git push`, or touch `terraform/envs/prod/`
- NEVER edit applied migrations or ADRs marked Accepted (add a new one)
- Ask before adding a dependency

## Definition of done
`make check` (lint + typecheck + test) passes, new code has tests, dbt models have tests + docs, ADR added for design changes.
