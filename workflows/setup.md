# First setup

Read the README and inspect `kit.toml`, `pyproject.toml` and setup scripts before running commands in a new checkout. Dependency installation and task definitions execute code; inspect unfamiliar changes to them like application changes.

Install Git, Python 3.12–3.14 and uv 0.13.1 through your approved tool distribution. Run `./scripts/setup.sh`, then `uv run --locked kit check` and `uv run --locked kit audit`.

The setup synchronizes a local `.venv` using `uv.lock`. It does not modify shell profiles, Git hooks, global assistant configuration or credentials. `./scripts/doctor.sh` reports missing requirements without repairing them.

Use [adoption instructions](../docs/adoption.md) when starting a new repository. Do not assume a directory called `workflows` is automatically loaded by an assistant.
