from pathlib import Path

import pytest

from agent_kit.config import find_root, load_config


def test_discovers_root_from_nested_directory(kit_root: Path) -> None:
    child = kit_root / "nested/src"
    child.mkdir(parents=True)
    assert find_root(child) == kit_root
    config = load_config(kit_root)
    assert config.checks == ("test",)
    assert config.tasks["test"].command[0] == "python"


def test_missing_root_is_actionable(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No kit.toml"):
        find_root(tmp_path)


@pytest.mark.parametrize(
    "before,after",
    [
        ('name = "test-kit"', "name = 1"),
        ('description = "test task"', 'description = ""'),
        ('command = ["python", "-c", "print(\'ok\')"]', 'command = "python -c something"'),
        ('tasks = ["test"]', 'tasks = ["missing"]'),
        ('command = ["python", "-c", "print(\'ok\')"]', "command = []"),
    ],
)
def test_invalid_configuration_is_rejected(kit_root: Path, before: str, after: str) -> None:
    path = kit_root / "kit.toml"
    path.write_text(path.read_text().replace(before, after))
    with pytest.raises(ValueError):
        load_config(kit_root)


def test_task_must_be_a_table(kit_root: Path) -> None:
    (kit_root / "kit.toml").write_text("""
[project]
name="x"
python="3.12"
uv="0.13.1"
[tasks]
bad="command"
""")
    with pytest.raises(ValueError, match="table"):
        load_config(kit_root)


@pytest.mark.parametrize("section", ["project", "tasks", "checks"])
def test_malformed_sections_fail_cleanly(kit_root: Path, section: str) -> None:
    content = (kit_root / "kit.toml").read_text()
    if section == "project":
        content = 'project="bad"\n'
    elif section == "tasks":
        content = content.split("[checks]")[0] + "\n[tasks.invalid]\ncommand=[]\n"
        content = content.split("[tasks.invalid]")[0].replace("[project]", 'tasks="bad"\n[project]')
    else:
        content = 'checks="bad"\n' + content.replace('[checks]\ntasks = ["test"]\n', "")
    (kit_root / "kit.toml").write_text(content)
    with pytest.raises(ValueError, match="table"):
        load_config(kit_root)
