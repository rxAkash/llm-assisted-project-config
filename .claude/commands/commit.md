---
description: Split the working-tree changes into small logical commits and make them one by one
argument-hint: "[optional focus, e.g. 'only .claude/' or 'ci']"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git restore --staged:*), Bash(git rev-parse:*)
---
Commit the current changes as a series of small, logical commits. Focus: $ARGUMENTS (if empty, all changes).

1. **Check the repo.** Run `git rev-parse --git-dir`. If this is not a git repository, stop and tell the user to run `git init` (do not run it yourself).
2. **Inspect.** Run `git status --porcelain`, `git diff`, `git diff --cached` and `git log --oneline -10` (to match the existing message style).
3. **Never stage secrets or local files:** `.env` and `.env.*` (except `.env.example`), `*.pem`, `*.tfstate*`, `.terraform/`, `.claude/settings.local.json`, caches and build output. If one shows up as untracked, warn the user and suggest a `.gitignore` entry instead.
4. **Plan.** Group the changes into commits that each do one thing and leave the repo working (for example: Makefile/tooling, Claude config, CI, dbt, docs). Show the plan as a numbered list: the files in each commit and its message. If one file mixes unrelated changes, say so and ask how to split it. **Wait for the user to approve or edit the plan before committing.**
5. **Commit one at a time.** For each commit in the plan:
   - Stage only its files by explicit path (`git add <paths>`). Never use `git add -A`, `git add .` or `git commit -a`.
   - Show `git diff --cached --stat` and confirm only the intended files are staged.
   - Commit with a Conventional Commits message: `type(scope): summary` (imperative, at most 72 chars; types: feat, fix, chore, ci, docs, refactor, test, build), plus a short body explaining *why* when it isn't obvious.
   - If a pre-commit hook fails: never use `--no-verify`. If the hook only reformatted files, re-stage those same files and commit again. Otherwise stop and report the failure.
   - Report the new commit's short hash and message, then move to the next one.
6. **Finish.** Show `git log --oneline` for the new commits and `git status` to confirm nothing intended was left behind. Never push.
