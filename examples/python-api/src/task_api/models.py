from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

Status = Literal["todo", "done"]
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class CreateTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Title


class UpdateTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Status


class Task(BaseModel):
    id: str
    title: str
    status: Status
