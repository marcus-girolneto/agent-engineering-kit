from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from task_api.app import create_app


def test_delete_contract(tmp_path: Path) -> None:
    database = tmp_path / "tasks.db"
    with TestClient(create_app(database)) as client:
        first = client.post("/tasks", json={"title": "remove"}).json()
        second = client.post("/tasks", json={"title": "keep"}).json()
        response = client.delete(f"/tasks/{first['id']}")
        assert response.status_code == 204
        assert response.content == b""
        assert client.delete(f"/tasks/{first['id']}").status_code == 404
        assert client.delete(f"/tasks/{uuid4()}").status_code == 404
        assert client.delete("/tasks/invalid").status_code == 422
    with TestClient(create_app(database)) as client:
        assert client.get(f"/tasks/{first['id']}").status_code == 404
        assert client.get(f"/tasks/{second['id']}").status_code == 200
