# Architecture

The root is a Python package exposing `kit`; `examples/python-api` is a separate uv workspace package. One lockfile resolves the workspace. Setup installs both packages and development tools. `kit.toml` is the command catalog, so local and CI checks use the same commands.

The CLI discovers `kit.toml` by walking up from the working directory. Configuration is validated before tasks run. Commands are argument arrays passed to `subprocess` without a shell. This prevents shell metacharacters from being interpreted but does not make an untrusted command safe.

`kit check` runs all configured checks, reports failures, then scans for secrets. It writes command exit codes and timing to `.artifacts/checks.json`. Individual checks can write coverage and JUnit artifacts. A failed check produces a nonzero exit code; checks are not silently skipped. Audit is separate because it requires network access and current advisory data.

The sample API uses a factory and lifespan initialization. Importing the module does not create a database. Each store operation owns a connection and closes it after commit or rollback. SQLite constraints provide another boundary behind request validation. Queries bind user input as parameters. Pagination uses insertion order, not random UUID order.

The kit has no agent orchestration runtime. It defines task instructions and contracts for assistants already running in a user's environment. See [the decision record](decisions/0001-instructions-and-checks.md).
