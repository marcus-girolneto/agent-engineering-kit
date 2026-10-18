import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query, Response

from .models import CreateTask, Status, Task, UpdateTask
from .store import TaskStore


def create_app(database: Path | None = None) -> FastAPI:
    store = TaskStore(database or Path(os.environ.get("TASK_DB_PATH", ".data/tasks.db")))

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        store.initialize()
        yield

    app = FastAPI(title="Task API", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/tasks", response_model=Task, status_code=201)
    def create_task(payload: CreateTask, response: Response) -> Task:
        task = store.create(payload.title)
        response.headers["Location"] = f"/tasks/{task.id}"
        return task

    @app.get("/tasks", response_model=list[Task])
    def list_tasks(
        status: Status | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> list[Task]:
        return store.list(status, limit, offset)

    @app.get("/tasks/{task_id}", response_model=Task)
    def get_task(task_id: UUID) -> Task:
        task = store.get(str(task_id))
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @app.patch("/tasks/{task_id}", response_model=Task)
    def update_task(task_id: UUID, payload: UpdateTask) -> Task:
        task = store.update(str(task_id), payload.status)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    return app
