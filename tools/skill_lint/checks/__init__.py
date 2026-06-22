"""Check registry. Each check maps a parsed ``SkillDoc`` to a list of ``Finding``.

A check reads its rule data from ``rules`` (loaded from rules.yaml) and emits a
finding only when the rule is not suppressed on that line.
"""

from __future__ import annotations

from skill_lint.core import Finding, Severity, SkillDoc


def make_finding(
    rules: dict,
    rule_id: str,
    doc: SkillDoc,
    line: int,
    *,
    message: str | None = None,
    hint: str | None = None,
) -> Finding:
    rule = rules["_by_id"][rule_id]
    return Finding(
        rule_id=rule_id,
        name=rule["name"],
        severity=Severity(rule["severity"]),
        path=str(doc.path),
        line=line,
        message=message or rule["message"],
        hint=hint if hint is not None else rule.get("hint"),
    )


# Imported after make_finding is defined so the submodules can import it back.
from skill_lint.checks.conditionals import check_conditionals  # noqa: E402
from skill_lint.checks.frontmatter import check_frontmatter  # noqa: E402
from skill_lint.checks.patterns import check_patterns  # noqa: E402
from skill_lint.checks.pronouns import check_pronouns  # noqa: E402
from skill_lint.checks.structure import check_structure  # noqa: E402

ALL_CHECKS = [
    check_frontmatter,
    check_pronouns,
    check_conditionals,
    check_patterns,
    check_structure,
]


def run_checks(doc: SkillDoc, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    for check in ALL_CHECKS:
        findings.extend(check(doc, rules))
    return findings
