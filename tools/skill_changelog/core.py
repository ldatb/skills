"""Pure parsing and rendering for conventional-commit changelogs."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Insertion order is the section order in the output — deterministic.
TYPES: dict[str, str] = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactors",
    "docs": "Documentation",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Chores",
    "style": "Style",
}

_CC = re.compile(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$")


@dataclass(frozen=True)
class Commit:
    type: str
    scope: str | None
    breaking: bool
    desc: str


def parse_commit(subject: str) -> Commit | None:
    """Parse a conventional-commit subject. Returns None if it is not one we track."""
    m = _CC.match(subject.strip())
    if not m:
        return None
    ctype = m.group("type").lower()
    if ctype not in TYPES:
        return None
    return Commit(
        type=ctype,
        scope=m.group("scope"),
        breaking=bool(m.group("breaking")),
        desc=m.group("desc").strip(),
    )


def _fmt(commit: Commit) -> str:
    scope = f"**{commit.scope}**: " if commit.scope else ""
    return f"- {scope}{commit.desc}"


def render_changelog(subjects: list[str], version: str, date: str | None = None) -> str:
    """Render a Keep-a-Changelog section. Deterministic in (subjects, version, date)."""
    commits = [c for s in subjects if (c := parse_commit(s)) is not None]
    groups: dict[str, list[Commit]] = {}
    for c in commits:
        groups.setdefault(c.type, []).append(c)

    header = f"## [{version}]" + (f" - {date}" if date else "")
    lines = [header, ""]

    breaking = [c for c in commits if c.breaking]
    if breaking:
        lines += ["### ⚠ BREAKING CHANGES", "", *[_fmt(c) for c in breaking], ""]

    for ctype, title in TYPES.items():
        if ctype in groups:
            lines += [f"### {title}", "", *[_fmt(c) for c in groups[ctype]], ""]

    return "\n".join(lines).rstrip() + "\n"


def prepend_section(existing: str | None, section: str) -> str:
    """Insert a new section above prior entries, keeping the top-level title."""
    title = "# Changelog\n"
    if not existing or "# Changelog" not in existing:
        return f"{title}\n{section}"
    head, _, rest = existing.partition("\n")
    # head is the '# Changelog' title line; rest is the remaining body.
    body = rest.lstrip("\n")
    return f"{head}\n\n{section}\n{body}".rstrip() + "\n"
