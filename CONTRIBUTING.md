# Contributing

Start with [AGENTS.md](AGENTS.md) and [setup](workflows/setup.md). Keep changes focused and document observable behavior. Use `uv run --locked kit check` before submitting; run `kit audit` for dependency changes.

Use Conventional Commits with a subject at most 72 characters:

```text
feat(api): add task deletion
fix(store): preserve insertion order during pagination
docs: explain the review workflow
test: cover transient tool failures
ci: update pinned checkout action
```

Breaking changes use `!` before the colon and explain the migration in the commit body. Common types are `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `style` and `revert`. PR titles follow the same format so squash commits remain conventional. Merge commits are excluded from history linting.

Describe the problem, the resulting behavior, actual checks and limitations. A review should lead with reproducible findings, not preferences. Report suspected vulnerabilities through [SECURITY.md](SECURITY.md).

Do not commit `.venv`, local databases, `.artifacts`, credentials or generated personal client settings. A secret-detector baseline entry needs a documented false-positive justification; broad exclusions require review.
