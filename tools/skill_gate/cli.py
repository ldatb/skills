"""Command-line entry point for skill-gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from skill_gate.core import Status, build_gates, detect_stacks, load_gates, run_gates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill-gate",
        description="Run deterministic engineering gates for a project's detected stack.",
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument(
        "--stack", action="append", help="Force a stack (repeatable). Default: auto-detect."
    )
    parser.add_argument(
        "--category", help="Only gates of this category (format/lint/types/sast/sca/secrets/test)."
    )
    parser.add_argument("--strict", action="store_true", help="A missing tool counts as a failure.")
    parser.add_argument(
        "--list", action="store_true", help="List the gates that would run; do not execute them."
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--gates", default=None, help="Path to an alternate gates.yaml.")
    args = parser.parse_args(argv)

    gates = load_gates(args.gates) if args.gates else load_gates()
    root = Path(args.root)
    stacks = args.stack or detect_stacks(root, gates)
    if not stacks:
        print("skill-gate: no known stack detected", file=sys.stderr)
        return 0

    gatelist = build_gates(stacks, gates, args.category)

    if args.list:
        for g in gatelist:
            print(f"{g.stack:12} {g.category:8} {g.id:18} {' '.join(g.cmd)}")
        return 0

    results = run_gates(gatelist, root, strict=args.strict)

    if args.format == "json":
        print(
            json.dumps(
                [
                    {
                        "stack": r.gate.stack,
                        "id": r.gate.id,
                        "category": r.gate.category,
                        "status": r.status.value,
                        "returncode": r.returncode,
                        "detail": r.detail,
                    }
                    for r in results
                ],
                indent=2,
            )
        )
    else:
        for r in results:
            head = f"[{r.status.value.upper():7}] {r.gate.stack}/{r.gate.id} ({r.gate.category})"
            first = r.detail.splitlines()[0] if r.detail else ""
            print(f"{head}  {first}".rstrip())
        counts = {s.value: sum(1 for r in results if r.status is s) for s in Status}
        print(
            f"\nskill-gate: {counts['pass']} pass, {counts['fail']} fail, "
            f"{counts['skipped']} skipped, {counts['error']} error"
            + ("  [strict]" if args.strict else "")
        )

    failed = sum(1 for r in results if r.status in (Status.FAIL, Status.ERROR))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
