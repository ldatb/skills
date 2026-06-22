"""Frontmatter checks (SK001–SK008): the skill's invocation contract."""

from __future__ import annotations

import re

from skill_lint.checks import make_finding
from skill_lint.core import Finding, SkillDoc

_KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _key_line(doc: SkillDoc, key: str, default: int = 1) -> int:
    pattern = re.compile(rf"^{re.escape(key)}\s*:")
    for ln in doc.lines:
        if ln.number > doc.fm_end_line:
            break
        if pattern.match(ln.text):
            return ln.number
    return default


def check_frontmatter(doc: SkillDoc, rules: dict) -> list[Finding]:
    settings = rules["settings"]
    out: list[Finding] = []
    fm = doc.frontmatter
    if fm is None:
        out.append(make_finding(rules, "SK001", doc, 1, message=doc.frontmatter_error))
        return out

    name = fm.get("name")
    if not name:
        out.append(make_finding(rules, "SK002", doc, 1))
    else:
        name = str(name)
        if not _KEBAB.match(name):
            out.append(make_finding(rules, "SK004", doc, _key_line(doc, "name")))
        if name != doc.folder_name:
            out.append(
                make_finding(
                    rules,
                    "SK003",
                    doc,
                    _key_line(doc, "name"),
                    message=f"Frontmatter 'name' ({name!r}) must equal folder name ({doc.folder_name!r}).",
                )
            )

    desc = fm.get("description")
    if not desc:
        out.append(make_finding(rules, "SK005", doc, 1))
    else:
        desc = str(desc)
        if len(desc) > settings["max_description_chars"]:
            out.append(
                make_finding(
                    rules,
                    "SK006",
                    doc,
                    _key_line(doc, "description"),
                    message=f"Description is {len(desc)} chars (max {settings['max_description_chars']}).",
                )
            )
        if not fm.get("disable-model-invocation"):
            low = desc.lower()
            if not any(trigger in low for trigger in settings["trigger_phrases"]):
                out.append(make_finding(rules, "SK007", doc, _key_line(doc, "description")))

    for key in fm:
        if key not in settings["allowed_frontmatter_keys"]:
            out.append(
                make_finding(
                    rules,
                    "SK008",
                    doc,
                    _key_line(doc, key),
                    message=f"Unrecognized frontmatter key: {key!r}.",
                )
            )
    return out
