"""Deterministic primitives shared by skills.

Skills call these instead of improvising file operations in prose. Each one
removes a class of ambiguity the agent would otherwise resolve non-deterministically:

- ``unique_path`` / ``unique_id`` — collision-free names guaranteed by the OS,
  not by the agent "making sure there are no collisions".
- ``atomic_write`` — readers never observe a half-written file.
- ``safe_remove`` — the ``rm -rf`` class of mistake is structurally impossible.
"""

from __future__ import annotations

from skillkit.fs import atomic_write, is_within, safe_remove
from skillkit.ids import unique_id, unique_path

__all__ = [
    "atomic_write",
    "is_within",
    "safe_remove",
    "unique_id",
    "unique_path",
]
