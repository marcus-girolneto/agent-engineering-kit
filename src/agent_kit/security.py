import json
import subprocess  # nosec B404
import tempfile
from pathlib import Path
from typing import Any

from .process import capture, execute

EXCLUDED = (
    r"(^|/)(\.git|\.venv|\.tooling|\.data|\.artifacts|\.mypy_cache|"
    r"\.pytest_cache|\.ruff_cache|__pycache__)/|(^|/)(uv\.lock|\.secrets\.baseline)$"
)


def fingerprints(scan: dict[str, Any]) -> set[tuple[str, str, str]]:
    return {
        (path, entry["type"], entry["hashed_secret"])
        for path, entries in scan.get("results", {}).items()
        for entry in entries
    }


def scan_secrets(root: Path) -> list[str]:
    output = capture(
        [
            "uv",
            "run",
            "--locked",
            "detect-secrets",
            "scan",
            "--all-files",
            "--no-verify",
            "--exclude-files",
            EXCLUDED,
        ],
        root,
    )
    scan = json.loads(output)
    baseline = json.loads((root / ".secrets.baseline").read_text())
    accepted = fingerprints(baseline)
    return [
        f"{path}:{entry['line_number']}: {entry['type']} (value redacted)"
        for path, entries in scan.get("results", {}).items()
        for entry in entries
        if (path, entry["type"], entry["hashed_secret"]) not in accepted
    ]


def audit_dependencies(root: Path) -> int:
    command = [
        "uv",
        "export",
        "--locked",
        "--all-packages",
        "--no-emit-workspace",
        "--format",
        "requirements-txt",
    ]
    exported = subprocess.run(  # nosec B603
        command, cwd=root, capture_output=True, text=True, check=False
    )
    if exported.returncode:
        print(exported.stderr)
        return exported.returncode
    with tempfile.TemporaryDirectory(prefix="kit-audit-") as directory:
        requirements = Path(directory) / "requirements.txt"
        requirements.write_text(exported.stdout)
        (root / ".artifacts").mkdir(exist_ok=True)
        result = execute(
            [
                "uv",
                "run",
                "--locked",
                "pip-audit",
                "--strict",
                "--progress-spinner",
                "off",
                "--require-hashes",
                "--disable-pip",
                "-r",
                str(requirements),
                "--format",
                "json",
                "--output",
                str(root / ".artifacts/audit.json"),
            ],
            root,
        )
    return int(result["exit_code"])
