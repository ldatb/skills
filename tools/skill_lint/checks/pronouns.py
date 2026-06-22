"""Pronoun ambiguity (SK010).

Flags a sentence that opens with a bare pronoun used as its subject
("It should…", "This causes…", "They are…"). A sentence-initial pronoun
followed immediately by a verb has no anchored referent, which is exactly where
an LLM's resolution turns non-deterministic. A qualified phrase ("This file…",
"These rules…") is fine and is not flagged.
"""

from __future__ import annotations

import re

from skill_lint.checks import make_finding
from skill_lint.core import Finding, SkillDoc, sentences

_WORD = re.compile(r"[A-Za-z']+")
_LEADING = " \t#-*>0123456789."


def check_pronouns(doc: SkillDoc, rules: dict) -> list[Finding]:
    settings = rules["settings"]
    pronouns = {p.lower() for p in settings["ambiguous_pronouns"]}
    verbs = {v.lower() for v in settings["pronoun_verbs"]}
    out: list[Finding] = []
    for ln in doc.prose_lines:
        stripped = ln.text.lstrip(_LEADING)
        for sentence in sentences(stripped):
            words = _WORD.findall(sentence)
            if len(words) >= 2 and words[0].lower() in pronouns and words[1].lower() in verbs:
                if not doc.is_suppressed(ln.number, "SK010"):
                    out.append(
                        make_finding(
                            rules,
                            "SK010",
                            doc,
                            ln.number,
                            message=f"Unanchored pronoun {words[0]!r} at sentence start — name the referent.",
                        )
                    )
                break
    return out
