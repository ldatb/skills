"""Pattern engine (SK020, SK040, SK041, SK050, SK060, SK080).

One deterministic regex pass drives every rule that carries a ``patterns`` list in
rules.yaml. A rule with ``scan_code: true`` is checked inside fenced code blocks
too (destructive commands and stray markers must not hide in examples); all other
pattern rules are natural-language and skip code fences.
"""

from __future__ import annotations

import re

from skill_lint.checks import make_finding
from skill_lint.core import Finding, SkillDoc


def check_patterns(doc: SkillDoc, rules: dict) -> list[Finding]:
    out: list[Finding] = []
    for rule in rules["rules"]:
        patterns = rule.get("patterns")
        if not patterns:
            continue
        compiled = [re.compile(p) for p in patterns]
        lines = doc.body_lines if rule.get("scan_code") else doc.prose_lines
        rule_id = rule["id"]
        for ln in lines:
            if any(rx.search(ln.text) for rx in compiled) and not doc.is_suppressed(
                ln.number, rule_id
            ):
                out.append(make_finding(rules, rule_id, doc, ln.number))
    return out
