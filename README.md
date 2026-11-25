# LLM Assisted Project Config
Snowflake -> Postgres replication, dbt, Airflow and a FastAPI service. See [AGENTS.md](AGENTS.md) for commands and conventions and [docs/architecture.md](docs/architecture.md) for the design.

## Prerequisites
Python 3.11, [uv](https://docs.astral.sh/uv/), Docker, Terraform >= 1.6, and Snowflake credentials.

## First-time setup
```sh
git init                 # if this isn't a git repo yet (pre-commit needs one)
make setup               # installs uv deps, creates .env from .env.example, installs pre-commit
# fill in .env
make check               # lint + typecheck + test
make up                  # local Postgres + API on :8000
```

## Claude Code
- Project instructions: `AGENTS.md` (imported by `CLAUDE.md`); permissions and hooks: `.claude/settings.json`.
- Commands: `/new-dag`, `/new-dbt-model`, `/new-tf-module`, `/review`, `/commit`; agent: `security-reviewer`.
- The GitHub MCP server (`.mcp.json`) needs a GitHub personal access token exported in your shell:
  `export GITHUB_PAT=...` before starting `claude`.
