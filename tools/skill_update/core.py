"""Pure version parsing and comparison for skill-update."""

from __future__ import annotations

import re

_VER = re.compile(r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?")


def parse_version(text: str) -> tuple[int, int, int] | None:
    """Parse a tag like 'v1.2.3' or '1.2' into a 3-tuple. None if unparseable."""
    m = _VER.match(text.strip())
    if not m:
        return None
    return tuple(int(g) if g else 0 for g in m.groups())  # type: ignore[return-value]


def is_newer(latest: str, current: str) -> bool:
    """True if ``latest`` is a strictly higher version than ``current``."""
    lv, cv = parse_version(latest), parse_version(current)
    if lv is None or cv is None:
        return False
    return lv > cv
