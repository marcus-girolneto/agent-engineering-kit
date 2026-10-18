import json
import shutil
from pathlib import Path

from agent_kit.documents import check_docs, validate_artifact

ROOT = Path(__file__).parents[1]


def test_links_and_instruction_budget(tmp_path: Path) -> None:
    (tmp_path / "exists.md").write_text("ok")
    (tmp_path / "README.md").write_text(
        "[ok](exists.md) [bad](missing.md) [web](https://example.org) [anchor](#a)\n"
        "```\n[example](not-a-real-file.md)\n```"
    )
    (tmp_path / "AGENTS.md").write_text("x" * 8193)
    errors = check_docs(tmp_path)
    assert len(errors) == 2
    assert any("8 KiB" in error for error in errors)
    assert any("missing.md" in error for error in errors)


def test_generated_directories_are_ignored(tmp_path: Path) -> None:
    directory = tmp_path / ".venv"
    directory.mkdir()
    (directory / "README.md").write_text("[bad](missing)")
    assert check_docs(tmp_path) == []


def test_review_contract_rejects_unsubstantiated_shapes(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    sample = json.loads((ROOT / "exercises/review/example-review.json").read_text())
    review = tmp_path / "review.json"
    review.write_text(json.dumps(sample))
    assert validate_artifact(tmp_path, "review", review) == []
    del sample["findings"][0]["evidence"]
    sample["checks"][0]["status"] = "probably passed"
    review.write_text(json.dumps(sample))
    assert len(validate_artifact(tmp_path, "review", review)) == 2


def test_no_findings_and_handoff_are_valid(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    review = tmp_path / "review.json"
    review.write_text(
        json.dumps(
            {
                "summary": "No actionable findings.",
                "findings": [],
                "checks": [],
                "limitations": ["Tests not run."],
            }
        )
    )
    assert validate_artifact(tmp_path, "review", review) == []
    handoff = tmp_path / "handoff.json"
    handoff.write_text(
        json.dumps(
            {
                "objective": "Document setup",
                "changes": ["README"],
                "checks": [],
                "risks": [],
                "next_steps": [],
            }
        )
    )
    assert validate_artifact(tmp_path, "handoff", handoff) == []
