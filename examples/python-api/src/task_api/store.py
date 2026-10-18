import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from .models import Status, Task


class TaskStore:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path, timeout=5)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    id TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
                    status TEXT NOT NULL CHECK(status IN ('todo', 'done'))
                )
            """)

    def create(self, title: str) -> Task:
        task = Task(id=str(uuid4()), title=title, status="todo")
        with self.connection() as connection:
            connection.execute(
                "INSERT INTO tasks (id, title, status) VALUES (?, ?, ?)",
                (task.id, task.title, task.status),
            )
        return task

    def get(self, task_id: str) -> Task | None:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
        return Task.model_validate(dict(row)) if row else None

    def list(self, status: Status | None, limit: int, offset: int) -> list[Task]:
        with self.connection() as connection:
            rows = connection.execute(
                "SELECT id, title, status FROM tasks WHERE (? IS NULL OR status = ?) "
                "ORDER BY sequence LIMIT ? OFFSET ?",
                (status, status, limit, offset),
            ).fetchall()
        return [Task.model_validate(dict(row)) for row in rows]

    def update(self, task_id: str, status: Status) -> Task | None:
        with self.connection() as connection:
            row = connection.execute(
                "UPDATE tasks SET status = ? WHERE id = ? RETURNING id, title, status",
                (status, task_id),
            ).fetchone()
        return Task.model_validate(dict(row)) if row else None
