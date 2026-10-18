# Task API example

This local API is a small codebase for practicing implementation, debugging and review. It persists tasks in SQLite and does not call an LLM.

From the repository root, after setup:

```bash
uv run --locked kit run serve
```

Open http://127.0.0.1:8000/docs for the generated API documentation, or create a task:

```bash
curl -sS http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Review the release notes"}'
```

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | Process liveness; not a database-readiness probe |
| `POST /tasks` | Create a task, trim title whitespace, return 201 and Location |
| `GET /tasks` | List by insertion order; optional status, limit 1–100 and nonnegative offset |
| `GET /tasks/{uuid}` | Retrieve a task or return 404 |
| `PATCH /tasks/{uuid}` | Set status to todo or done; repeating the same update is harmless |

Titles must contain 1–200 characters after trimming. Unknown request fields are rejected. Malformed identifiers return 422. SQL is parameterized and each operation closes its database connection. Tests use temporary databases; the server defaults to `.data/tasks.db` or the exported `TASK_DB_PATH` variable. Environment files are not loaded automatically.

There is no authentication, tenant model, public ingress limit, migration framework or backup service. The supplied command binds to loopback. Do not treat it as a public production deployment. See [the threat model](../../docs/threat-model.md) before changing that boundary.
