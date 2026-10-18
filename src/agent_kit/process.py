import shlex
import subprocess  # nosec B404
import time
from pathlib import Path
from typing import Any


def capture(command: list[str], root: Path) -> str:
    result = subprocess.run(  # nosec B603
        command, cwd=root, text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"Command failed: {command[0]}")
    return result.stdout


def execute(command: list[str], root: Path) -> dict[str, Any]:
    print(f"$ {shlex.join(command)}", flush=True)
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=root, check=False)  # nosec B603
        code = result.returncode
    except FileNotFoundError:
        print(f"Missing executable: {command[0]}", flush=True)
        code = 127
    return {"command": command, "exit_code": code, "seconds": round(time.monotonic() - started, 3)}
