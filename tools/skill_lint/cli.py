"""Command-line entry point for skill-lint."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from skill_lint.checks import run_checks
from skill_lint.core import Finding, Severity, SkillDoc, load_rules

try:
    from skillkit import atomic_write
except ImportError:  # pragma: no cover - skillkit is always present in this repo
    atomic_write = None


def discover(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(p.rglob("SKILL.md")))
        elif p.is_file():
            files.append(p)
    # de-duplicate while preserving order
    seen: set[Path] = set()
    unique: list[Path] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def _autofix(path: Path) -> list[str]:
    """Apply only deterministic, unambiguously-safe fixes. Returns descriptions."""
    fixes: list[str] = []
    doc = SkillDoc.load(path)
    if doc.frontmatter is None:
        return fixes
    raw = path.read_text(encoding="utf-8")
    name = str(doc.frontmatter.get("name", ""))
    if name and name != doc.folder_name:
        new_raw = re.sub(
            r"^name:\s*.*$",
            f"name: {doc.folder_name}",
            raw,
            count=1,
            flags=re.MULTILINE,
        )
        if new_raw != raw:
            raw = new_raw
            fixes.append(f"name -> {doc.folder_name}")
    if not raw.endswith("\n"):
        raw += "\n"
        fixes.append("added final newline")
    if fixes and atomic_write is not None:
        atomic_write(path, raw)
    return fixes


def _render_text(findings: list[Finding]) -> str:
    lines = []
    for f in findings:
        hint = f"  (hint: {f.hint})" if f.hint else ""
        lines.append(
            f"{f.path}:{f.line}: [{f.severity.value.upper()} {f.rule_id} {f.name}] {f.message}{hint}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill-lint",
        description="Deterministic linter for SKILL.md files — wrings ambiguity out of skills.",
    )
    parser.add_argument("paths", nargs="*", help="Files or directories (default: skills/).")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures too.")
    parser.add_argument("--fix", action="store_true", help="Apply deterministic autofixes.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--rules", default=None, help="Path to an alternate rules.yaml.")
    args = parser.parse_args(argv)

    rules = load_rules(args.rules) if args.rules else load_rules()
    files = discover(args.paths or ["skills"])

    if not files:
        print("skill-lint: no SKILL.md files found", file=sys.stderr)
        return 0

    if args.fix:
        for path in files:
            for desc in _autofix(path):
                print(f"fixed {path}: {desc}")

    findings: list[Finding] = []
    for path in files:
        findings.extend(run_checks(SkillDoc.load(path), rules))
    findings.sort(key=lambda f: f.sort_key())

    threshold = Severity.WARNING.rank if args.strict else Severity.ERROR.rank
    failed = sum(1 for f in findings if f.severity.rank >= threshold)

    if args.format == "json":
        print(
            json.dumps(
                [
                    {
                        "path": f.path,
                        "line": f.line,
                        "rule_id": f.rule_id,
                        "name": f.name,
                        "severity": f.severity.value,
                        "message": f.message,
                        "hint": f.hint,
                    }
                    for f in findings
                ],
                indent=2,
            )
        )
    else:
        if findings:
            print(_render_text(findings))
        counts = {s.value: sum(1 for f in findings if f.severity is s) for s in Severity}
        print(
            f"\nskill-lint: {len(files)} file(s), "
            f"{counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info"
            + ("  [strict]" if args.strict else "")
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
