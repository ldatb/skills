"""The scaffolder must emit a skill that passes the linter under --strict."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from skill_lint.checks import run_checks
from skill_lint.core import SkillDoc, load_rules
from skill_new.cli import main

RULES = load_rules()


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    return tmp_path


def test_scaffold_is_lint_clean_user(tmp_path):
    root = _repo(tmp_path)
    assert main(["--category", "engineering", "--name", "my-skill", "--root", str(root)]) == 0
    skill = root / "skills" / "engineering" / "my-skill" / "SKILL.md"
    assert skill.exists()
    findings = run_checks(SkillDoc.load(skill), RULES)
    assert findings == [], [f"{f.rule_id}:{f.message}" for f in findings]


def test_scaffold_is_lint_clean_model(tmp_path):
    root = _repo(tmp_path)
    main(
        [
            "--category",
            "engineering",
            "--name",
            "auto-skill",
            "--invocation",
            "model",
            "--root",
            str(root),
        ]
    )
    skill = root / "skills" / "engineering" / "auto-skill" / "SKILL.md"
    findings = run_checks(SkillDoc.load(skill), RULES)
    assert findings == [], [f"{f.rule_id}:{f.message}" for f in findings]


def test_scaffold_registers_in_manifest(tmp_path):
    root = _repo(tmp_path)
    main(["--category", "personal", "--name", "journal", "--root", str(root)])
    manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text())
    assert "./skills/personal/journal" in manifest["skills"]


def test_scaffold_refuses_overwrite(tmp_path):
    root = _repo(tmp_path)
    main(["--category", "personal", "--name", "dup", "--root", str(root)])
    with pytest.raises(SystemExit):
        main(["--category", "personal", "--name", "dup", "--root", str(root)])


def test_scaffold_rejects_non_kebab(tmp_path):
    root = _repo(tmp_path)
    with pytest.raises(SystemExit):
        main(["--category", "engineering", "--name", "Bad_Name", "--root", str(root)])
