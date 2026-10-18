import argparse
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

from .commits import check_commits, validate_subject
from .config import Config, find_root, load_config
from .documents import check_docs, validate_artifact
from .process import capture, execute
from .security import audit_dependencies, scan_secrets


def doctor(root: Path, config: Config) -> int:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("Python", (3, 12) <= sys.version_info[:2] < (3, 15), sys.version.split()[0]))
    for tool in ("git", "uv"):
        executable = shutil.which(tool)
        checks.append((tool, bool(executable), executable or "not found on PATH"))
    if shutil.which("uv"):
        version = capture(["uv", "--version"], root).split()[1]
        checks.append(("uv version", version == config.uv, f"{version}; required {config.uv}"))
    checks.append(("lockfile", (root / "uv.lock").is_file(), "uv.lock"))
    checks.append(("environment", (root / ".venv/pyvenv.cfg").is_file(), "run setup if missing"))
    git_root = root / ".git"
    checks.append(("Git checkout", git_root.exists(), "needed for history checks"))
    for name, ok, detail in checks:
        print(f"{'OK' if ok else 'FAIL':4} {name}: {detail}")
    print("Doctor reads configuration; it does not install tools or print environment values.")
    return int(any(not ok for _, ok, _ in checks))


def report_errors(errors: list[str]) -> int:
    for error in errors:
        print(error)
    if not errors:
        print("OK")
    return int(bool(errors))


def run_checks(root: Path, config: Config) -> int:
    results = []
    for name in config.checks:
        result = execute(list(config.tasks[name].command), root)
        results.append({"task": name, **result})
    try:
        secrets = scan_secrets(root)
        secret_status = report_errors(secrets)
    except (OSError, ValueError) as exc:
        print(f"Secret scan could not complete: {type(exc).__name__}")
        secret_status = 2
    results.append({"task": "secrets", "exit_code": secret_status})
    report = {"created_at": datetime.now(UTC).isoformat(), "checks": results}
    directory = root / ".artifacts"
    directory.mkdir(exist_ok=True)
    (directory / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
    return int(any(result["exit_code"] != 0 for result in results))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Set up, verify and review an agent-ready repository."
    )
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("setup", "doctor", "check", "tasks", "docs", "secrets", "audit"):
        commands.add_parser(name)
    run = commands.add_parser("run")
    run.add_argument("task")
    commits = commands.add_parser("commits")
    commits.add_argument("--base")
    commits.add_argument("--head", default="HEAD")
    commits.add_argument("--subject")
    artifact = commands.add_parser("validate")
    artifact.add_argument("kind", choices=["review", "handoff"])
    artifact.add_argument("file", type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        root = find_root(Path.cwd())
        config = load_config(root)
        if args.command == "doctor":
            return doctor(root, config)
        if args.command == "setup":
            if not shutil.which("uv"):
                raise ValueError(f"Install uv {config.uv} first; see README.md")
            return int(execute(["uv", "sync", "--locked", "--all-packages"], root)["exit_code"])
        if args.command == "tasks":
            for name, task in config.tasks.items():
                print(f"{name:18} {task.description}")
            return 0
        if args.command == "run":
            if args.task not in config.tasks:
                raise ValueError(f"Unknown task: {args.task}. Run kit tasks.")
            return int(execute(list(config.tasks[args.task].command), root)["exit_code"])
        if args.command == "check":
            return run_checks(root, config)
        if args.command == "docs":
            return report_errors(check_docs(root))
        if args.command == "secrets":
            return report_errors(scan_secrets(root))
        if args.command == "audit":
            return audit_dependencies(root)
        if args.command == "commits":
            if args.subject is not None:
                error = validate_subject(args.subject)
                return report_errors([error] if error else [])
            return report_errors(check_commits(root, args.base, args.head))
        return report_errors(validate_artifact(root, args.kind, args.file))
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
