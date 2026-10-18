# Development exercise: task deletion

Add `DELETE /tasks/{task_id}` to the example API. Deleting an existing task returns 204 with an empty body. Deleting an unknown UUID returns 404; malformed IDs return 422. The task must remain deleted after restarting the app against the same database. Other tasks must remain intact.

Follow [the development workflow](../../workflows/development.md). Add your own focused tests, then run the supplied acceptance check:

```bash
uv run --locked pytest exercises/development/acceptance.py -q
```

The acceptance check intentionally fails on the unmodified template because deletion is not implemented. It is not part of the default passing test suite. Do not modify the acceptance check to accommodate the implementation.

Finish with `kit check`, a Conventional Commit subject and a handoff recording the checks actually run. Consider how deletion would change in a multi-tenant production service; do not add an unrequested authentication framework to this local exercise.
