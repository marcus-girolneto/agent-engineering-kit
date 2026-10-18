import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    description: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class Config:
    name: str
    python: str
    uv: str
    checks: tuple[str, ...]
    tasks: dict[str, Task]


def find_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "kit.toml").is_file():
            return candidate
    raise ValueError("No kit.toml found. Run this command inside the kit repository.")


def load_config(root: Path) -> Config:
    raw = tomllib.loads((root / "kit.toml").read_text())
    project = raw.get("project", {})
    if not isinstance(project, dict):
        raise ValueError("project must be a table")
    values = [project.get(key) for key in ("name", "python", "uv")]
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValueError("project.name, project.python and project.uv must be nonempty strings")
    tasks = {}
    task_config = raw.get("tasks", {})
    if not isinstance(task_config, dict):
        raise ValueError("tasks must be a table")
    for name, value in task_config.items():
        if not isinstance(value, dict):
            raise ValueError(f"Task {name} must be a table")
        command, description = value.get("command"), value.get("description")
        if not isinstance(description, str) or not description:
            raise ValueError(f"Task {name} needs a description")
        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(arg, str) and arg and "\x00" not in arg for arg in command)
        ):
            raise ValueError(
                f"Task {name} needs a nonempty argument array; shell strings are rejected"
            )
        tasks[name] = Task(description, tuple(command))
    check_config = raw.get("checks", {})
    if not isinstance(check_config, dict):
        raise ValueError("checks must be a table")
    checks = check_config.get("tasks", [])
    if (
        not isinstance(checks, list)
        or not checks
        or not all(isinstance(name, str) and name in tasks for name in checks)
    ):
        raise ValueError("checks.tasks must name existing tasks")
    return Config(project["name"], project["python"], project["uv"], tuple(checks), tasks)
