# Security

Version 0.1 receives fixes on `main`. This is a local development template, not a hardened public service. Read [the threat model](docs/threat-model.md) for assumptions and coverage.

Report suspected vulnerabilities through [GitHub private vulnerability reporting](https://github.com/marcus-girolneto/agent-engineering-kit/security/advisories/new). Include affected revision, preconditions, a minimal reproduction with synthetic data and likely impact. Do not publish active secrets or run an exploit against a third-party system.

If private reporting is unavailable in a fork, contact that repository's maintainers through an established private channel. Enable private reporting when adopting the template. There is no guaranteed response SLA.

The `exercises/review/fixtures` directory intentionally contains vulnerable code for a local exercise. It is not part of the packaged API. Its documented SQL weaknesses are known training material; an unintended path into a running application would be a reportable issue.
