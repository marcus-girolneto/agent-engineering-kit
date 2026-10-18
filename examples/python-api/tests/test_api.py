from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from task_api.app import create_app
from task_api.store import TaskStore


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    with TestClient(create_app(tmp_path / "tasks.db")) as client:
        yield client


def test_create_read_and_complete_task(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "  Review the change  "})
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Review the change"
    assert task["status"] == "todo"
    assert response.headers["location"] == f"/tasks/{task['id']}"
    assert client.get(response.headers["location"]).json() == task
    done = client.patch(response.headers["location"], json={"status": "done"})
    assert done.status_code == 200
    assert done.json()["status"] == "done"
    assert client.patch(response.headers["location"], json={"status": "done"}).json() == done.json()


@pytest.mark.parametrize("title", ["", "   ", "x" * 201, None, 42])
def test_invalid_titles_are_rejected(client: TestClient, title: object) -> None:
    assert client.post("/tasks", json={"title": title}).status_code == 422
    assert client.get("/tasks").json() == []


def test_unknown_fields_and_status_are_rejected(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "ok", "owner": "admin"}).status_code == 422
    task = client.post("/tasks", json={"title": "ok"}).json()
    assert client.patch(f"/tasks/{task['id']}", json={"status": "deleted"}).status_code == 422
    assert (
        client.patch(f"/tasks/{task['id']}", json={"status": "done", "id": "x"}).status_code == 422
    )


def test_filter_and_pagination_have_stable_order(client: TestClient) -> None:
    tasks = [client.post("/tasks", json={"title": str(i)}).json() for i in range(3)]
    client.patch(f"/tasks/{tasks[0]['id']}", json={"status": "done"})
    assert [t["id"] for t in client.get("/tasks?status=todo").json()] == [
        tasks[1]["id"],
        tasks[2]["id"],
    ]
    assert client.get("/tasks?limit=1&offset=1").json() == [tasks[1]]
    assert client.get("/tasks?status=done").json()[0]["id"] == tasks[0]["id"]


@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1", "status=missing"])
def test_unbounded_or_invalid_list_requests_fail(client: TestClient, query: str) -> None:
    assert client.get(f"/tasks?{query}").status_code == 422


def test_unknown_and_invalid_ids(client: TestClient) -> None:
    url = f"/tasks/{uuid4()}"
    assert client.get(url).status_code == 404
    assert client.patch(url, json={"status": "done"}).status_code == 404
    assert client.get("/tasks/not-a-uuid").status_code == 422


def test_sql_payload_is_stored_as_text(client: TestClient) -> None:
    title = "'); DROP TABLE tasks; --"
    response = client.post("/tasks", json={"title": title})
    assert response.status_code == 201
    assert response.json()["title"] == title
    assert len(client.get("/tasks").json()) == 1


def test_data_survives_application_restart(tmp_path: Path) -> None:
    path = tmp_path / "tasks.db"
    with TestClient(create_app(path)) as first:
        task = first.post("/tasks", json={"title": "persist"}).json()
    with TestClient(create_app(path)) as second:
        assert second.get(f"/tasks/{task['id']}").json() == task
        assert second.get("/health").json() == {"status": "ok"}


def test_factory_respects_environment_without_writing_on_import(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / "nested/tasks.db"
    monkeypatch.setenv("TASK_DB_PATH", str(path))
    app = create_app()
    assert not path.exists()
    with TestClient(app):
        assert path.exists()


def test_failed_transaction_rolls_back(tmp_path: Path) -> None:
    store = TaskStore(tmp_path / "tasks.db")
    store.initialize()
    with pytest.raises(RuntimeError), store.connection() as connection:
        connection.execute(
            "INSERT INTO tasks (id, title, status) VALUES (?, ?, ?)",
            (str(uuid4()), "rollback", "todo"),
        )
        raise RuntimeError("simulate failure")
    assert store.list(None, 20, 0) == []
