"""Command-line entry point for skill-docs."""

from __future__ import annotations

import argparse
import json

from skill_docs.core import check_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill-docs",
        description="Check that relative links and file references in Markdown resolve.",
    )
    parser.add_argument(
        "paths", nargs="*", help="Files or directories (default: current directory)."
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    files, broken = check_paths(args.paths or ["."])

    if args.format == "json":
        print(
            json.dumps(
                [{"path": b.path, "line": b.line, "target": b.target} for b in broken], indent=2
            )
        )
    else:
        for b in broken:
            print(f"{b.path}:{b.line}: broken link -> {b.target}")
        print(f"\nskill-docs: {len(files)} file(s), {len(broken)} broken link(s)")

    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
