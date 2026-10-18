# Security controls and exceptions

| Control | Enforced by | Scope |
| --- | --- | --- |
| Input and state validation | Pydantic, SQLite constraints, tests | Sample API requests and stored task state |
| SQL parameter binding | Store implementation and exploit-payload test | All executable sample store queries |
| Secret detection | detect-secrets with verification disabled | Local files excluding generated/tool/data directories and lock/baseline files |
| Known dependency advisories | pip-audit with a hashed uv export | Locked runtime and development dependencies; remote advisory service required |
| Python static security checks | Bandit | Kit and sample application source |
| Workflow supply chain | Action commit SHA pins, read-only token, no persisted checkout credentials | Checked-in GitHub workflows |
| Conventional Commits | `kit commits`, CI and PR-title check | Non-merge commit subjects and squash-merge titles |
| Branch rules, push protection | GitHub repository settings | Must be checked per repository; not inherited from template files |

## Narrow exceptions

Bandit B404 and B603 are suppressed only on the reviewed subprocess imports/call sites in `process.py` and `security.py`. The runner intentionally executes argument arrays from trusted repository configuration; the audit command is constructed from fixed arguments. Neither uses a shell. Tests demonstrate that shell metacharacters remain literal arguments and nonzero exits propagate. This does not make a malicious executable or task configuration safe. No project-wide Bandit rule is disabled.

`exercises/review/fixtures` contains intentionally vulnerable source. It is excluded from application lint, type and Bandit targets, is outside packaged source directories, and is executed only in a synthetic in-memory regression exercise. Secret detection still includes it.

The secret scanner excludes `.git`, virtual environments, caches, `.data`, `.artifacts`, `uv.lock` and its own baseline. Lockfiles contain package hashes that create entropy false positives; review source indexes/URLs when changing a lockfile. Data and artifact paths are ignored by Git and must not hold distributable credentials. The scanner does not prove ignored/generated data is safe. It disables live credential verification to avoid sending candidate values to external services.

The baseline begins empty. Add an entry only after confirming that an individual fingerprint is a false positive, and record the justification here. Never approve a whole file because one line was a false positive. Changed values and different file paths remain detectable.

Audit records contain dependency metadata, not source or credentials. Advisory results are time-sensitive; a clean audit means no known advisories were returned for that exact dependency set at the time checked.
