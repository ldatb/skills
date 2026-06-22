"""Structural hygiene (SK070): guard against sprawl."""

from __future__ import annotations

from skill_lint.checks import make_finding
from skill_lint.core import Finding, SkillDoc


def check_structure(doc: SkillDoc, rules: dict) -> list[Finding]:
    limit = rules["settings"]["max_skill_lines"]
    non_empty = [ln for ln in doc.body_lines if ln.text.strip()]
    if len(non_empty) <= limit:
        return []
    line = doc.fm_end_line + 1 if doc.fm_end_line else 1
    if doc.is_suppressed(line, "SK070"):
        return []
    return [
        make_finding(
            rules,
            "SK070",
            doc,
            line,
            message=f"SKILL.md body is {len(non_empty)} non-empty lines (max {limit}); disclose reference to linked files.",
        )
    ]
