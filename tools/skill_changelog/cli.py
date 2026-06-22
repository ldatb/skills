"""Command-line entry point for skill-changelog (git access + optional write)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from skill_changelog.core import prepend_section, render_changelog
from skillkit import atomic_write


def git_subjects(from_ref: str | None, to_ref: str, root: str) -> list[str]:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git not found on PATH")
    rng = f"{from_ref}..{to_ref}" if from_ref else to_ref
    proc = subprocess.run(  # noqa: S603 - absolute path, argv list, shell=False
        [git, "-C", str(root), "log", "--pretty=%s", rng],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in proc.stdout.splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill-changelog",
        description="Generate a CHANGELOG section from conventional commits.",
    )
    parser.add_argument("--version", required=True, help="Version label for the new section.")
    parser.add_argument("--from", dest="from_ref", default=None, help="Start ref, exclusive (default: repo start).")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="End ref (default: HEAD).")
    parser.add_argument("--date", default=None, help="Optional date for the section header.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", default=None, metavar="FILE", help="Prepend the section to FILE.")
    args = parser.parse_args(argv)

    try:
        subjects = git_subjects(args.from_ref, args.to_ref, args.root)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"skill-changelog: {exc}", file=sys.stderr)
        return 1

    section = render_changelog(subjects, args.version, args.date)

    if args.write:
        path = Path(args.write)
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        atomic_write(path, prepend_section(existing, section))
        print(f"wrote {path}")
    else:
        print(section, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
