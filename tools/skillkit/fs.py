"""Filesystem operations with the dangerous interpretations removed.

``atomic_write`` and ``safe_remove`` exist so a skill never has to phrase a file
mutation in prose an agent could misread. ``safe_remove`` in particular makes the
``rm -rf`` class structurally impossible: it refuses anything outside its root,
refuses the root itself, and never recurses.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
from pathlib import Path


def _resolve(path: str | os.PathLike[str]) -> Path:
    return Path(path).expanduser().resolve()


def is_within(root: str | os.PathLike[str], path: str | os.PathLike[str]) -> bool:
    """True if ``path`` is ``root`` or lives beneath it (symlinks resolved)."""
    root_r = _resolve(root)
    path_r = _resolve(path)
    return path_r == root_r or root_r in path_r.parents


def atomic_write(
    path: str | os.PathLike[str],
    data: str | bytes,
    *,
    encoding: str = "utf-8",
) -> Path:
    """Write ``data`` to ``path`` atomically: a reader sees the old file or the new, never a partial one.

    Writes to a temp file in the same directory, fsyncs, then ``os.replace`` (atomic
    on POSIX and Windows). Parent directories are created as needed.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    is_bytes = isinstance(data, bytes)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(
            fd, "wb" if is_bytes else "w", encoding=None if is_bytes else encoding
        ) as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp)
        raise
    return path


def safe_remove(path: str | os.PathLike[str], *, root: str | os.PathLike[str]) -> bool:
    """Remove a single file, symlink, or empty directory — only inside ``root``.

    Returns True if something was removed, False if the path did not exist. Raises
    ``ValueError`` for anything outside ``root`` or for ``root`` itself, and
    ``OSError`` for a non-empty directory (it never recurses). This is the
    deterministic guard against accidental mass deletion.
    """
    raw_abs = Path(os.path.abspath(os.path.expanduser(str(path))))
    root_real = _resolve(root)
    target_real = _resolve(raw_abs)
    if raw_abs == root_real or target_real == root_real:
        raise ValueError(f"refusing to remove root itself: {raw_abs}")
    if root_real not in target_real.parents:
        raise ValueError(f"refusing to remove outside root: {target_real} not under {root_real}")
    if raw_abs.is_symlink():
        raw_abs.unlink()
        return True
    if not raw_abs.exists():
        return False
    if raw_abs.is_dir():
        os.rmdir(raw_abs)  # non-empty -> OSError, by design (never recursive)
    else:
        raw_abs.unlink()
    return True
