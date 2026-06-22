"""Command-line entry point for skill-update (GitHub tag check)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from importlib.metadata import PackageNotFoundError, version

from skill_update.core import is_newer

REPO = "ldatb/skills"
PACKAGE = "ldatb-skills-tools"


def installed_version() -> str | None:
    try:
        return version(PACKAGE)
    except PackageNotFoundError:
        return None


def latest_tag(repo: str, timeout: int = 10) -> str | None:
    url = f"https://api.github.com/repos/{repo}/tags"
    req = urllib.request.Request(  # noqa: S310 - fixed https GitHub API host
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "skill-update"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        data = json.load(resp)
    return data[0]["name"] if data else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill-update", description="Check for a newer toolchain release on GitHub."
    )
    parser.add_argument("--repo", default=REPO, help=f"owner/name (default: {REPO}).")
    args = parser.parse_args(argv)

    current = installed_version()
    if current is None:
        print(
            "skill-update: toolchain is not installed as a package; run scripts/install.sh",
            file=sys.stderr,
        )
        return 1

    try:
        latest = latest_tag(args.repo)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        print(f"skill-update: could not reach GitHub ({exc})", file=sys.stderr)
        return 1

    if latest is None:
        print(f"skill-update: no tags found for {args.repo}; installed {current}")
        return 0

    if is_newer(latest, current):
        print(
            f"update available: {current} -> {latest}\n"
            f"  update with: uv tool install --force git+https://github.com/{args.repo}"
        )
    else:
        print(f"up to date: {current} (latest {latest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
