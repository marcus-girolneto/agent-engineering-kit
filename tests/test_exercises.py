import importlib.util
import sqlite3
from pathlib import Path

FIXTURE = Path(__file__).parents[1] / "exercises/review/fixtures/unsafe_store.py"


def test_review_fixture_has_reproducible_cross_account_access() -> None:
    spec = importlib.util.spec_from_file_location("unsafe_fixture", FIXTURE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE tasks (id TEXT, owner TEXT, title TEXT, status TEXT)")
        connection.executemany(
            "INSERT INTO tasks VALUES (?, ?, ?, ?)",
            [
                ("a", "alice", "private a", "todo"),
                ("b", "bob", "private b", "todo"),
            ],
        )
        assert len(module.list_tasks(connection, "alice")) == 1
        assert len(module.list_tasks(connection, "' OR 1=1 --")) == 2
        module.complete_task(connection, "b", "alice")
        assert connection.execute("SELECT status FROM tasks WHERE id = 'b'").fetchone()[0] == "done"
    finally:
        connection.close()
