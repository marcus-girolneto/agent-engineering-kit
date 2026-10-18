# Validation record

This document records checks performed during initial development. It is a dated observation, not a promise that a future dependency set or deployment is secure. The CI badge and workflow artifacts show the current revision's results.

Initial local checks on 2026-10-18 use Python 3.12 on macOS and uv 0.13.1. The local gate passed 61 tests with 99.33% statement/branch coverage, along with Ruff lint/format, strict mypy checks, Bandit, local link checks and secret detection. A separate pip-audit run returned no known advisories for the locked dependencies. These are scoped observations, not proof of security.

The repository contains behavior tests for the CLI, configuration, commit history, review contracts, secret-detector integration, the deliberately vulnerable review exercise and the sample API.

The development acceptance check is intentionally separate and fails before the deletion feature is implemented. This is part of the exercise contract, not a failing default test suite.

Resolved dependency versions are recorded in `uv.lock`. CI runs the same local gate on Linux with Python 3.12, 3.13 and 3.14. Dependency audits include runtime and development packages and are performed against live advisory data; artifacts retain the exact package results. No LLM calls or agent-performance measurements were made.
