"""Pure link discovery and resolution checks for Markdown."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_LINK = re.compile(r"\]\(([^)]+)\)")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class BrokenLink:
    path: str
    line: int
    target: str


def find_links(text: str) -> list[tuple[int, str]]:
    """Return (line_number, target) for every Markdown link outside fenced code blocks."""
    out: list[tuple[int, str]] = []
    in_code = False
    for i, line in enumerate(text.splitlines(), start=1):
        if _FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in _LINK.finditer(line):
            out.append((i, m.group(1).strip()))
    return out


def is_local(target: str) -> bool:
    """True for repo-relative targets — the only ones we can resolve deterministically."""
    if not target:
        return False
    if target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return False
    return "://" not in target


def check_file(path: str | Path) -> list[BrokenLink]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    broken: list[BrokenLink] = []
    for line, target in find_links(text):
        if not is_local(target):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue  # pure in-page anchor
        if not (path.parent / clean).exists():
            broken.append(BrokenLink(str(path), line, target))
    return broken


def check_paths(paths: list[str]) -> tuple[list[Path], list[BrokenLink]]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
        elif p.suffix == ".md":
            files.append(p)
    broken: list[BrokenLink] = []
    for f in files:
        broken.extend(check_file(f))
    return files, broken
