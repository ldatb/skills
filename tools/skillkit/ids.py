"""Collision-free identifiers and file paths.

The "make sure there are no collisions" instruction is ambiguous: an agent may
satisfy it by checking-then-creating (a race) or, catastrophically, by deleting
whatever is already there. These helpers remove the ambiguity — uniqueness is
guaranteed by 122 bits of entropy and, for files, by an atomic ``O_EXCL`` create.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path


def unique_id(prefix: str = "") -> str:
    """Return a collision-free identifier (uuid4 hex, optionally prefixed)."""
    token = uuid.uuid4().hex
    return f"{prefix}{token}" if prefix else token


def unique_path(
    directory: str | os.PathLike[str],
    prefix: str = "",
    suffix: str = "",
    *,
    max_attempts: int = 10_000,
) -> Path:
    """Reserve and return a brand-new file path, created empty and atomically.

    Uses ``O_CREAT | O_EXCL`` so the path is guaranteed not to have existed, even
    under concurrent callers. The created file is the caller's to fill. Safe to run
    in parallel: the kernel — not the agent — enforces uniqueness.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for _ in range(max_attempts):
        candidate = directory / f"{prefix}{uuid.uuid4().hex}{suffix}"
        try:
            fd = os.open(candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            continue
        os.close(fd)
        return candidate
    raise RuntimeError(
        f"could not reserve a unique path in {directory} after {max_attempts} attempts"
    )
