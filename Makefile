.PHONY: setup env fmt lint typecheck test check up down dbt-build tf-plan
ENV ?= dev
# Run every tool from the project venv created by `uv sync`
RUN := uv run

setup: env
	command -v uv >/dev/null || pip install uv
	uv sync --all-extras
	@if git rev-parse --git-dir >/dev/null 2>&1; then \
		$(RUN) pre-commit install; \
	else \
		echo "Not a git repository: run 'git init' and then 'make setup' again to install the pre-commit hooks"; \
	fi
env:
	@test -f .env || { cp .env.example .env && echo "Created .env from .env.example: fill in the values"; }
fmt:
	$(RUN) ruff format . && $(RUN) ruff check --fix .
lint:
	$(RUN) ruff check . && $(RUN) ruff format --check . && $(RUN) sqlfluff lint dbt/models --dialect snowflake
typecheck:
	$(RUN) mypy ingestion/src api/app
test:
	$(RUN) pytest ingestion/tests api/tests airflow/tests -q
check: lint typecheck test
up: env
	docker compose up -d --build
down:
	docker compose down -v
dbt-build:
	cd dbt && $(RUN) dbt build
tf-plan:
	cd terraform/envs/$(ENV) && terraform init -backend=false && terraform plan
