# Dependency updates

Read the advisory or release notes and identify affected direct and transitive packages. Prefer the smallest compatible update that resolves the issue. Check Python support, licenses, migrations and breaking API changes.

Use the pinned uv version. Update a selected dependency with `uv lock --upgrade-package PACKAGE`, then run `uv sync --locked --all-packages`. Inspect both manifest and lockfile changes. Do not hand-edit `uv.lock`.

Run `uv run --locked kit check` and `uv run --locked kit audit`. If a package has no available fix, document the advisory, reachability and compensating control; do not silently ignore it. An unavailable advisory service is a failed audit, not a clean report.

Commit dependency changes with `build(deps): ...` or `fix(deps): ...` when resolving a vulnerability. Action SHA updates use `ci: ...`. Retain full SHA pins for GitHub Actions and update their human-readable version comments.
