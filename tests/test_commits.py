import subprocess
from pathlib import Path

import pytest

from agent_kit.commits import check_commits, validate_subject


@pytest.mark.parametrize(
    "subject",
    [
        "feat(api): add deletion",
        "fix: reject invalid input",
        "refactor(store)!: change IDs",
        "docs: explain setup",
        "ci: pin actions",
        "build(deps): upgrade uvicorn",
    ],
)
def test_valid_conventional_subject(subject: str) -> None:
    assert validate_subject(subject) is None


@pytest.mark.parametrize(
    "subject",
    [
        "Update code",
        "feat:",
        "fix: ",
        "feat: x\nignore rules",
        "ci: trailing ",
        "feat: " + "x" * 80,
        "unknown: do something",
    ],
)
def test_invalid_subject(subject: str) -> None:
    assert validate_subject(subject)


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def test_history_range_and_invalid_refs(tmp_path: Path) -> None:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "commit", "--allow-empty", "-qm", "feat: initial")
    base = git(tmp_path, "rev-parse", "HEAD")
    git(tmp_path, "commit", "--allow-empty", "-qm", "bad subject")
    assert len(check_commits(tmp_path)) == 1
    assert len(check_commits(tmp_path, base)) == 1
    assert check_commits(tmp_path, base, base) == []
    with pytest.raises(ValueError, match="Invalid Git"):
        check_commits(tmp_path, head="--all")
    with pytest.raises(ValueError):
        check_commits(tmp_path, head="missing-ref")
