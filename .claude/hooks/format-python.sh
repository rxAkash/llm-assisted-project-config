#!/usr/bin/env bash
# PostToolUse hook: format only the edited file, and only if it is Python.
# Formatting failures never block Claude, so this always exits 0.
file=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
case "$file" in
  *.py) uv run --quiet ruff format --quiet "$file" >/dev/null 2>&1 ;;
esac
exit 0
