# Development

1. Read `git status --short`, the task and the nearest relevant instructions. Inspect the code and tests before designing a change. State the observable acceptance criteria and any assumption that affects behavior.
2. Trace the existing request/data path. Reuse established boundaries. For a cross-cutting change, identify migration, compatibility and rollback needs before editing.
3. Implement one coherent change. Keep generated files reproducible; update the lockfile only when dependencies change. Add a focused behavior test for the new contract and important failure paths.
4. Run the focused test first. Then run `uv run --locked kit check`. Run `uv run --locked kit audit` when dependencies change; it needs network access.
5. Inspect the final diff for unintended edits, credentials, changed public behavior and missing docs. Use [definition of done](../checklists/definition-of-done.md).
6. Hand off the outcome, commands and their actual results, and remaining risks. Use [the handoff schema](../schemas/handoff.schema.json) when machine-readable output is requested.

Do not add architecture layers for a hypothetical future requirement. Do not run a formatter over unrelated files to hide a small change. A successful local test does not establish deployment readiness.

Example task: [add task deletion](../exercises/development/task.md).
