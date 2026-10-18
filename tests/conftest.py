from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


@pytest.fixture
def kit_root(tmp_path: Path) -> Path:
    (tmp_path / "kit.toml").write_text("""
[project]
name = "test-kit"
python = "3.12"
uv = "0.13.1"
[checks]
tasks = ["test"]
[tasks.test]
description = "test task"
command = ["python", "-c", "print('ok')"]
""")
    (tmp_path / ".secrets.baseline").write_text('{"results": {}}')
    return tmp_path
