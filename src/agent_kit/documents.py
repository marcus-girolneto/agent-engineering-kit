import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator

SKIP = {".git", ".venv", ".tooling", ".artifacts", ".mypy_cache", ".pytest_cache", ".ruff_cache"}


def check_docs(root: Path) -> list[str]:
    errors = []
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP for part in path.relative_to(root).parts):
            continue
        text = path.read_text()
        if path.name == "AGENTS.md" and len(text.encode()) > 8192:
            errors.append(f"{path.relative_to(root)}: keep automatic instructions under 8 KiB")
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", prose):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"{path.relative_to(root)}: broken local link {target}")
    return errors


def validate_artifact(root: Path, kind: str, path: Path) -> list[str]:
    schema = json.loads((root / "schemas" / f"{kind}.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    value = json.loads(path.read_text())
    return [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema).iter_errors(value)
    ]
