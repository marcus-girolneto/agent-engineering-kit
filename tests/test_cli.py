import json
import sys
from pathlib import Path

import pytest

from agent_kit import cli
from agent_kit.config import load_config
from agent_kit.process import capture, execute


def test_commands_are_arguments_not_shell_programs(tmp_path: Path) -> None:
    sentinel = tmp_path / "should-not-exist"
    argument = f"; touch {sentinel}"
    assert (
        capture(
            [sys.executable, "-c", "import sys; print(sys.argv[1])", argument], tmp_path
        ).strip()
        == argument
    )
    assert not sentinel.exists()
    assert execute([sys.executable, "-c", "raise SystemExit(7)"], tmp_path)["exit_code"] == 7
    assert execute(["kit-deliberately-missing-executable"], tmp_path)["exit_code"] == 127
    with pytest.raises(ValueError):
        capture([sys.executable, "-c", "raise SystemExit(1)"], tmp_path)


def invoke(monkeypatch, root: Path, *args: str) -> int:
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "argv", ["kit", *args])
    return cli.main()


def test_task_catalog_and_unknown_task(kit_root: Path, monkeypatch, capsys) -> None:
    assert invoke(monkeypatch, kit_root, "tasks") == 0
    assert "test task" in capsys.readouterr().out
    assert invoke(monkeypatch, kit_root, "run", "missing") == 2
    assert "Unknown task" in capsys.readouterr().err


def test_task_exit_status_and_setup(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "execute", lambda *args: {"exit_code": 7})
    assert invoke(monkeypatch, kit_root, "run", "test") == 7
    monkeypatch.setattr(cli.shutil, "which", lambda _: "/bin/uv")
    assert invoke(monkeypatch, kit_root, "setup") == 7
    monkeypatch.setattr(cli.shutil, "which", lambda _: None)
    assert invoke(monkeypatch, kit_root, "setup") == 2


def test_checks_continue_after_failure_and_write_report(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "execute", lambda *args: {"exit_code": 1, "seconds": 0.1})
    monkeypatch.setattr(cli, "scan_secrets", lambda _: [])
    assert invoke(monkeypatch, kit_root, "check") == 1
    report = json.loads((kit_root / ".artifacts/checks.json").read_text())
    assert [r["task"] for r in report["checks"]] == ["test", "secrets"]
    assert report["checks"][1]["exit_code"] == 0


def test_doctor_is_read_only_and_detects_version_mismatch(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda name: f"/bin/{name}")
    monkeypatch.setattr(cli, "capture", lambda *args: "uv 0.0.0")
    before = set(kit_root.rglob("*"))
    assert cli.doctor(kit_root, load_config(kit_root)) == 1
    assert set(kit_root.rglob("*")) == before
    (kit_root / "uv.lock").touch()
    (kit_root / ".venv").mkdir()
    (kit_root / ".venv/pyvenv.cfg").touch()
    (kit_root / ".git").mkdir()
    monkeypatch.setattr(cli, "capture", lambda *args: "uv 0.13.1")
    assert invoke(monkeypatch, kit_root, "doctor") == 0


@pytest.mark.parametrize("command,function", [("docs", "check_docs"), ("secrets", "scan_secrets")])
def test_validation_exit_codes(kit_root: Path, monkeypatch, command: str, function: str) -> None:
    monkeypatch.setattr(cli, function, lambda _: ["failure"])
    assert invoke(monkeypatch, kit_root, command) == 1


def test_subject_and_artifact_validation_routes(kit_root: Path, monkeypatch) -> None:
    assert invoke(monkeypatch, kit_root, "commits", "--subject", "feat: add something") == 0
    assert invoke(monkeypatch, kit_root, "commits", "--subject", "bad") == 1
    monkeypatch.setattr(cli, "check_commits", lambda *args: [])
    assert invoke(monkeypatch, kit_root, "commits") == 0
    monkeypatch.setattr(cli, "validate_artifact", lambda *args: [])
    assert invoke(monkeypatch, kit_root, "validate", "review", "review.json") == 0
    monkeypatch.setattr(cli, "audit_dependencies", lambda _: 1)
    assert invoke(monkeypatch, kit_root, "audit") == 1


def test_interrupt_returns_shell_convention(kit_root: Path, monkeypatch) -> None:
    def interrupt(*args):
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "check_docs", interrupt)
    assert invoke(monkeypatch, kit_root, "docs") == 130


def test_scanner_failure_is_not_reported_as_clean(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "execute", lambda *args: {"exit_code": 0})

    def unavailable(root):
        raise ValueError("detector failed")

    monkeypatch.setattr(cli, "scan_secrets", unavailable)
    assert invoke(monkeypatch, kit_root, "check") == 1
    report = json.loads((kit_root / ".artifacts/checks.json").read_text())
    assert report["checks"][-1]["exit_code"] == 2
