#!/usr/bin/env python3
"""Validate drafted content against per-platform format, length, and ratio limits.

The agent writes the content and picks the platform; this script enforces the
constraints the SKILL names in prose, so the agent never re-checks a caption
length, a hashtag count, or an aspect ratio by eye. The limits below are the
single source of truth for the platform-fit gate.

Spec shape (JSON):

    {"items": [
        {"platform": "x|instagram|linkedin|tiktok|youtube",
         "caption": "...",
         "hashtags": ["growth", "saas"],
         "aspect": "9:16"}
    ]}

  content-lint.py check <spec.json>   -> validate every item, exit 1 on any violation
  content-lint.py --selftest          -> assert against fixtures, exit 0

Read-only. Exit code is the verdict.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

# --- the constant table: the platform-fit limits, in one place ------------
# caption: maximum caption length in characters.
# hashtags: maximum hashtag count (a hard cap; the SKILL names softer norms).
# aspects: the allowed aspect ratios for that platform.
_PLATFORMS: dict[str, dict[str, object]] = {
    "x": {"caption": 280, "hashtags": 3, "aspects": ("16:9", "1:1", "9:16")},
    "instagram": {"caption": 2200, "hashtags": 30, "aspects": ("1:1", "4:5", "9:16")},
    "linkedin": {"caption": 3000, "hashtags": 10, "aspects": ("1:1", "4:5", "16:9")},
    "tiktok": {"caption": 2200, "hashtags": 10, "aspects": ("9:16",)},
    "youtube": {"caption": 5000, "hashtags": 15, "aspects": ("16:9", "9:16")},
}


def _violations_for(index: int, item: object) -> list[str]:
    """Return the violation lines for one content item (empty list when clean)."""
    label = f"item[{index}]"
    if not isinstance(item, dict):
        return [f"{label}: not an object"]
    platform = item.get("platform")
    if not isinstance(platform, str) or platform not in _PLATFORMS:
        known = ", ".join(sorted(_PLATFORMS))
        return [f"{label}: unknown platform {platform!r} (known: {known})"]

    limits = _PLATFORMS[platform]
    found: list[str] = []
    where = f"{label} ({platform})"

    caption = item.get("caption", "")
    if not isinstance(caption, str):
        found.append(f"{where}: caption must be a string")
    else:
        cap_max = int(limits["caption"])
        if len(caption) > cap_max:
            found.append(f"{where}: caption {len(caption)} chars exceeds {cap_max}")

    hashtags = item.get("hashtags", [])
    if not isinstance(hashtags, list):
        found.append(f"{where}: hashtags must be a list")
    else:
        tag_max = int(limits["hashtags"])
        if len(hashtags) > tag_max:
            found.append(f"{where}: {len(hashtags)} hashtags exceeds cap of {tag_max}")

    aspect = item.get("aspect")
    allowed = tuple(limits["aspects"])
    if aspect is not None and (not isinstance(aspect, str) or aspect not in allowed):
        found.append(f"{where}: aspect {aspect!r} not in {list(allowed)}")
    return found


def lint(spec: object) -> list[str]:
    """Return every violation across the spec's items (empty list when clean)."""
    if not isinstance(spec, dict):
        return ["spec: top level must be a JSON object"]
    items = spec.get("items")
    if not isinstance(items, list):
        return ["spec: 'items' must be a list"]
    violations: list[str] = []
    for index, item in enumerate(items):
        violations.extend(_violations_for(index, item))
    return violations


def _load(spec_path: str) -> tuple[object | None, str | None]:
    """Load and parse the spec; return (spec, error_message)."""
    path = Path(spec_path)
    if not path.is_file():
        return None, f"error: spec is not a file: {spec_path}"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"error: cannot read spec: {exc}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"error: spec is not valid JSON: {exc}"


def check(spec_path: str) -> int:
    """Validate the spec file; print violations, return the exit code."""
    spec, error = _load(spec_path)
    if error is not None:
        print(error, file=sys.stderr)
        return 2
    violations = lint(spec)
    if not violations:
        print("content-lint: ok")
        return 0
    print(f"content-lint: {len(violations)} violation(s)", file=sys.stderr)
    for line in violations:
        print(f"  {line}", file=sys.stderr)
    return 1


def selftest() -> int:
    """Assert a clean item passes and each limit breach is flagged, then exit 0."""
    assert lint({"items": []}) == []
    clean = {
        "items": [
            {"platform": "x", "caption": "short and sharp", "hashtags": ["build"]},
            {"platform": "tiktok", "caption": "hook", "hashtags": [], "aspect": "9:16"},
        ]
    }
    assert lint(clean) == [], lint(clean)

    over_caption = {"items": [{"platform": "x", "caption": "z" * 281, "hashtags": []}]}
    flagged = lint(over_caption)
    assert any("caption" in v and "exceeds" in v for v in flagged), flagged

    over_tags = {"items": [{"platform": "instagram", "caption": "ok", "hashtags": ["t"] * 31}]}
    flagged = lint(over_tags)
    assert any("hashtags exceeds" in v for v in flagged), flagged

    wrong_aspect = {"items": [{"platform": "tiktok", "caption": "ok", "aspect": "16:9"}]}
    flagged = lint(wrong_aspect)
    assert any("aspect" in v for v in flagged), flagged

    bad_platform = {"items": [{"platform": "myspace", "caption": "ok"}]}
    assert any("unknown platform" in v for v in lint(bad_platform)), lint(bad_platform)

    assert lint({"items": "nope"}) == ["spec: 'items' must be a list"]
    assert lint("nope") == ["spec: top level must be a JSON object"]

    # The boundary path: a missing file and bad JSON are each rejected with a
    # nonzero exit. The deliberate-failure stderr is captured so a passing
    # selftest stays quiet, per the script standard.
    with tempfile.TemporaryDirectory(prefix="content-lint-selftest.") as tmp:
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured), contextlib.redirect_stdout(captured):
            missing_code = check(str(Path(tmp) / "absent.json"))
            bad = Path(tmp) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            bad_code = check(str(bad))
            good = Path(tmp) / "good.json"
            good.write_text(json.dumps(clean), encoding="utf-8")
            good_code = check(str(good))
        assert missing_code == 2, captured.getvalue()
        assert bad_code == 2, captured.getvalue()
        assert good_code == 0, captured.getvalue()

    print("content-lint selftest: ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true", help="Run the self-test and exit.")
    sub = parser.add_subparsers(dest="command")
    check_parser = sub.add_parser("check", help="Validate a content spec file.")
    check_parser.add_argument("spec", help="Path to the content spec JSON file.")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.command == "check":
        return check(args.spec)
    parser.error("a command is required (check) unless --selftest is given")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
