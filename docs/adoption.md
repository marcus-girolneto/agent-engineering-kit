# Adopt the template

1. Use GitHub's **Use this template** button, or clone the repository and point `origin` to your new project. Inspect the files before setup.
2. Replace the repository name and badge/issue/security links in `README.md`, `SECURITY.md` and `.github/ISSUE_TEMPLATE/config.yml`. Replace `.github/CODEOWNERS` with your maintainers. Keep the original MIT attribution when redistributing the kit.
3. Update `project.name` in `kit.toml`, package metadata and the project map in `AGENTS.md`. Keep executable commands aligned with the actual stack. Remove the example workspace member and its dependencies only if you are replacing the example.
4. Run setup, the local gate and the dependency audit. Confirm the selected assistant loads the instructions using [the integration guide](agent-integrations.md).
5. Configure your GitHub repository: protect `main`, require successful verification and audit checks, disable force pushes, prefer squash merges and require an appropriate reviewer for your team. These hosting rules do not travel with template files. A solo maintainer should explicitly choose an emergency/bypass policy.
6. Enable private vulnerability reporting and GitHub secret scanning/push protection where available. Check repository settings after creation; the template cannot enforce account-level features.
7. Review Dependabot access and any notifications. Exercise the development and review tasks before applying the kit to production code.

## Commands

| Command | Behavior |
| --- | --- |
| `./scripts/setup.sh` | Synchronize the locked workspace and diagnose prerequisites |
| `./scripts/doctor.sh` | Read environment state without syncing dependencies |
| `uv run --locked kit tasks` | List configured tasks |
| `uv run --locked kit check` | Lint, formatting, types, tests, static analysis, docs, secrets |
| `uv run --locked kit audit` | Query known advisories for locked runtime and development dependencies |
| `uv run --locked kit commits` | Check all reachable non-merge commit subjects |
| `uv run --locked kit commits --base BASE --head HEAD` | Check only a selected history range |
| `uv run --locked kit validate review FILE` | Validate a review's structure |
| `uv run --locked kit validate handoff FILE` | Validate a handoff's structure |

`uv run` may synchronize the local environment. Use `doctor.sh` for a read-only environment check. The `.env.example` file documents variables; no automatic dotenv loader is installed. Export variables explicitly. Do not put credentials in task definitions.

On Windows, use uv directly (`uv sync --locked --all-packages`, then `uv run --locked kit doctor`). Shell wrappers target macOS/Linux. Python packages support 3.12–3.14; the CI matrix validates Linux on those versions.
