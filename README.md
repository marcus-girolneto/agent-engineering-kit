# Agent Engineering Kit

[![CI](https://github.com/marcus-girolneto/agent-engineering-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/marcus-girolneto/agent-engineering-kit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12–3.14-blue)](pyproject.toml)
[![MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A working repository template for building software with coding agents. It gives an assistant a project map, focused workflows and commands whose results can be checked by a person or CI.

The useful contract is simple: understand the task, make a bounded change, verify observable behavior, and report the evidence. The kit makes that contract executable without requiring an agent framework or an API key.

## Start in five minutes

Prerequisites: Git, Python 3.12–3.14 and **uv 0.13.1**. Install that uv version through your approved package manager, for example `pipx install uv==0.13.1`. See [uv installation](https://docs.astral.sh/uv/getting-started/installation/) for alternatives.

Use **Use this template** on GitHub, or:

```bash
git clone https://github.com/marcus-girolneto/agent-engineering-kit.git
cd agent-engineering-kit
./scripts/setup.sh
uv run --locked kit check
```

The gate runs lint, formatting, strict type checks, behavior tests, static security analysis, local documentation checks and secret detection. It writes results to `.artifacts/`. It needs no model credentials. Dependency installation needs network access; after setup, the local checks do not call an LLM or an advisory service.

Run the separate dependency audit when network access is available:

```bash
uv run --locked kit audit
```

For a container environment, open the repository in a client supporting [Dev Containers](.devcontainer/devcontainer.json). The container runs as a non-root user, drops Linux capabilities, keeps its Python environment separate from the host and does not mount a Docker socket or credential directory. See [container setup](docs/container.md).

## What is included

| Layer | Files | Purpose |
| --- | --- | --- |
| Agent context | [AGENTS.md](AGENTS.md), small client bridges | Give the assistant commands, boundaries and a project map |
| Task workflows | [Development](workflows/development.md), [review](workflows/code-review.md), [debugging](workflows/debugging.md), [security](workflows/security-review.md) | Define how work is performed and handed off |
| Execution | [kit.toml](kit.toml), `kit` CLI | Use the same command catalog locally and in CI |
| Reproducible setup | `uv.lock`, `.python-version`, setup and doctor scripts | Pin dependencies and make missing prerequisites visible |
| Deliverables | [Review](schemas/review.schema.json) and [handoff](schemas/handoff.schema.json) schemas | Require structured evidence and explicit limitations |
| Real example | [Task API](examples/python-api/README.md) | Exercise validation, persistence, SQL boundaries and tests |
| Practice | [Development](exercises/development/task.md), [debugging](exercises/debugging/task.md), [review](exercises/review/task.md) | Demonstrate the workflow with inspectable acceptance criteria |
| Security | [Threat model](docs/threat-model.md), [controls](docs/security-controls.md), audit, secret detector | State what is enforced and what remains outside the kit |

## A normal development session

Give your assistant a concrete task:

```text
Read AGENTS.md and workflows/development.md.
Implement exercises/development/task.md.
Preserve the acceptance contract and report the checks actually run.
```

The task adds deletion to the sample API. It has an explicit acceptance test that fails on the unchanged template and should pass after implementation. The ordinary repository gate passes before the exercise; the exercise test is separate.

For a review-only session:

```text
Read AGENTS.md and workflows/code-review.md.
Review exercises/review/task.md without editing the fixture.
Return JSON matching schemas/review.schema.json.
```

Validate a review's format:

```bash
uv run --locked kit validate review exercises/review/example-review.json
```

The schema validates structure. It cannot tell whether a finding is true or whether a claimed test actually ran. The review exercise includes an answer key and reproducible vulnerabilities so that reasoning can be checked.

## Commands you will use

```bash
./scripts/doctor.sh                       # read-only environment diagnosis
uv run --locked kit tasks                # list available tasks
uv run --locked kit run test             # behavior tests and coverage
uv run --locked kit run serve            # local API at 127.0.0.1:8000
uv run --locked kit check                # local verification gate
uv run --locked kit audit                # networked dependency advisory check
uv run --locked kit commits              # Conventional Commits history check
```

Commands in `kit.toml` are argument arrays, not shell strings. Review them before executing an unfamiliar checkout: an argument array still launches the configured program.

## Agent integration

Codex uses the root `AGENTS.md`. `CLAUDE.md` and `.github/copilot-instructions.md` provide small bridges to the same guidance. Read [integration details](docs/agent-integrations.md) and confirm what your client actually loads. No global client settings, hooks, MCP servers or credentials are installed.

Workflows are documents read on demand. They do not launch autonomous agents. Permission enforcement belongs to the assistant runtime and hosting platform.

## Security and scope

CI uses read-only GitHub permissions, action SHA pins and disposable hosted runners. The kit checks secrets, known dependency advisories, unsafe Python patterns and API behavior. [Security controls](docs/security-controls.md) documents precise scope and narrow exceptions.

The sample API is local and unauthenticated. The review exercise intentionally contains vulnerable code outside packaged application source. This repository is not a security certification or a ready-to-deploy multi-tenant service.

GitHub branch rules, private reporting and push protection are repository settings; they do not travel with a template. Review [adoption steps](docs/adoption.md) before using the kit for a real project.

## Design and evidence

- [Architecture](docs/architecture.md) and [decision record](docs/decisions/0001-instructions-and-checks.md)
- [Validation record](docs/records/validation.md)
- [Contribution and commit conventions](CONTRIBUTING.md)
- [Security reporting](SECURITY.md)

This kit verifies its tooling and example behavior. It does not claim to improve agent accuracy without a separate controlled evaluation. To measure an agent's decisions, pair the workflow with a benchmark such as [Agent Reliability Lab](https://github.com/marcus-girolneto/agent-reliability-lab).
