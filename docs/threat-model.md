# Threat model

## Assets and actors

The kit protects source integrity, local credentials, review accuracy and CI artifacts. The example stores synthetic task titles in a local SQLite file. Actors include the developer, a coding assistant with local tool access, a contributor submitting a pull request, a package publisher, and text supplied in issues or tool output.

| Boundary | Failure mode | Control here | Remaining limitation |
| --- | --- | --- | --- |
| User request → agent | Scope expands into production changes | Explicit authority rules and bounded workflows | Instructions do not enforce a runtime sandbox |
| Logs/issues/files → agent | Prompt injection changes the task or requests secrets | Evidence/instruction separation and a review exercise | Model compliance is not formally guaranteed |
| Task configuration → process | Untrusted config executes a malicious program | Argument arrays, no shell interpolation, config review | A configured executable can still run arbitrary code |
| HTTP input → SQLite | SQL injection and invalid state | Parameterized queries, strict schemas, database constraints and tests | No authentication; do not expose the example publicly |
| Pull request → CI | Exfiltration through privileged workflows | `pull_request`, read-only token, no repository secrets, pinned actions | Untrusted tests still execute code; use hosted disposable runners |
| Dependencies → environment | Compromised package or known vulnerability | Committed lockfile, hashes, advisory audit and Dependabot | Locking does not prove publisher trust; advisory databases lag |
| Files → Git | Credential accidentally committed | Ignore rules and local secret detector | Pattern detection has false negatives; ignored files are not guaranteed safe |
| Review output → decision | Fabricated findings or test claims | Evidence fields, schema and human review | Schema validation cannot establish semantic truth |

## Deliberate boundaries

The API binds to 127.0.0.1 in the provided task and has no authentication. It is an example for local synthetic data. Public deployment requires an authentication and authorization design, ingress/body limits, rate limiting, monitoring, backups and migrations.

The kit does not install an MCP server, provision cloud resources, change global assistant approval settings or send source code to an LLM. Using an external coding assistant has its own data handling and permission model.

The review fixture contains deliberately unsafe SQL. It is excluded from application lint/type/security scans, never packaged as an application module, and exercised only against an in-memory test database. Secret detection still scans the fixture.

## Verification

Tests cover malformed inputs, SQL payloads, persistence, transaction rollback, task-runner exit codes, commit validation and review schema rejection. The default gate runs without an LLM or API key. Dependency audit uses a remote advisory service. The doc checker validates local file links, not external availability or heading anchors.

For a real incident, revoke exposed credentials, preserve evidence and follow the owning system's response process. The kit is not a replacement for an incident-response program.
