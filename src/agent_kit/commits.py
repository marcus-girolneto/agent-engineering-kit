import re
from pathlib import Path

from .process import capture

SUBJECT = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([a-z0-9][a-z0-9._/-]*\))?!?: \S.*$"
)


def validate_subject(subject: str) -> str | None:
    if len(subject) > 72:
        return "subject exceeds 72 characters"
    if "\n" in subject or "\r" in subject or not SUBJECT.fullmatch(subject):
        return "use type(scope): description, for example fix(api): reject blank titles"
    if subject != subject.rstrip():
        return "subject has trailing whitespace"
    return None


def check_commits(root: Path, base: str | None = None, head: str = "HEAD") -> list[str]:
    refs = []
    for ref in [base, head] if base else [head]:
        if ref is None or ref.startswith("-"):
            raise ValueError("Invalid Git reference")
        refs.append(capture(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], root).strip())
    revision = f"{refs[0]}..{refs[1]}" if base else refs[0]
    output = capture(["git", "log", "--no-merges", "--format=%h%x09%s", revision], root)
    errors = []
    for line in output.splitlines():
        commit, subject = line.split("\t", 1)
        if error := validate_subject(subject):
            errors.append(f"{commit}: {error} ({subject})")
    return errors
