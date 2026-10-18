import hashlib
import json
import subprocess
from pathlib import Path

from agent_kit import security


def test_detector_finds_synthetic_key_without_verifying_it(tmp_path: Path) -> None:
    key = "AKIA" + "J" * 16
    (tmp_path / "config.txt").write_text("aws_access_key_id = " + key)
    result = subprocess.run(
        ["detect-secrets", "scan", "--all-files", "--no-verify"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    scan = json.loads(result.stdout)
    assert scan["results"]["config.txt"]
    assert key not in result.stdout


def test_baseline_matching_is_scoped_and_does_not_print_secret(kit_root: Path, monkeypatch) -> None:
    entry = {
        "type": "Secret Keyword",
        "hashed_secret": hashlib.sha256(b"first fixture").hexdigest(),
        "line_number": 4,
    }
    scan = {"results": {"config.py": [entry]}}
    monkeypatch.setattr(security, "capture", lambda *args: json.dumps(scan))
    assert security.scan_secrets(kit_root) == ["config.py:4: Secret Keyword (value redacted)"]
    (kit_root / ".secrets.baseline").write_text(json.dumps(scan))
    assert security.scan_secrets(kit_root) == []
    entry["line_number"] = 40
    assert security.scan_secrets(kit_root) == []
    entry["hashed_secret"] = hashlib.sha256(b"second fixture").hexdigest()
    assert security.scan_secrets(kit_root)


def test_audit_uses_hashed_export_and_propagates_status(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        security.subprocess,
        "run",
        lambda *a, **kw: subprocess.CompletedProcess(a[0], 0, "package==1 --hash=sha256:abc", ""),
    )
    captured = []

    def execute(command, root):
        requirements = Path(command[command.index("-r") + 1])
        captured.append(requirements.read_text())
        assert "--require-hashes" in command
        assert "--disable-pip" in command
        return {"exit_code": 1}

    monkeypatch.setattr(security, "execute", execute)
    assert security.audit_dependencies(kit_root) == 1
    assert captured == ["package==1 --hash=sha256:abc"]


def test_audit_export_failure_stops_before_audit(kit_root: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        security.subprocess,
        "run",
        lambda *a, **kw: subprocess.CompletedProcess(a[0], 2, "", "lock mismatch"),
    )
    assert security.audit_dependencies(kit_root) == 2
