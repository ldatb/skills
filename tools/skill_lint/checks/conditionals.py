"""Conditional complexity (SK030).

More than one conditional keyword in a single sentence is compound branching the
agent may execute only some of the time. The fix is to split each branch into its
own step, or to move the decision into a script.
"""

from __future__ import annotations

import re

from skill_lint.checks import make_finding
from skill_lint.core import Finding, SkillDoc, sentences


def check_conditionals(doc: SkillDoc, rules: dict) -> list[Finding]:
    rule = rules["_by_id"]["SK030"]
    limit = rules["settings"]["max_conditionals_per_sentence"]
    keywords = [re.compile(k) for k in rule["keywords"]]
    out: list[Finding] = []
    for ln in doc.prose_lines:
        for sentence in sentences(ln.text.lower()):
            count = sum(1 for kw in keywords if kw.search(sentence))
            if count > limit and not doc.is_suppressed(ln.number, "SK030"):
                out.append(make_finding(rules, "SK030", doc, ln.number))
                break
    return out
