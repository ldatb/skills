"""Parsing and rendering are deterministic and total over the cases we care about."""

from __future__ import annotations

from skill_changelog.core import parse_commit, prepend_section, render_changelog


def test_parse_plain():
    c = parse_commit("feat: add widget")
    assert c is not None and c.type == "feat" and c.desc == "add widget" and not c.breaking


def test_parse_scope_and_breaking():
    c = parse_commit("fix(api)!: drop legacy field")
    assert c is not None and c.type == "fix" and c.scope == "api" and c.breaking


def test_parse_non_conventional_is_none():
    assert parse_commit("just some message") is None


def test_parse_unknown_type_is_none():
    assert parse_commit("wip: scratch") is None


def test_render_groups_and_orders():
    out = render_changelog(["feat: a", "fix: b", "feat: c"], "1.0.0")
    assert "## [1.0.0]" in out
    assert "### Features" in out and "### Bug Fixes" in out
    # Features come before Bug Fixes (TYPES insertion order).
    assert out.index("### Features") < out.index("### Bug Fixes")
    assert "- a" in out and "- c" in out and "- b" in out


def test_render_breaking_section():
    out = render_changelog(["feat!: big change"], "2.0.0", date="2026-06-22")
    assert "## [2.0.0] - 2026-06-22" in out
    assert "BREAKING CHANGES" in out


def test_render_is_deterministic():
    subjects = ["feat: a", "fix(x): b", "chore: c"]
    assert render_changelog(subjects, "1.1.0") == render_changelog(subjects, "1.1.0")


def test_render_ignores_noise():
    out = render_changelog(["feat: a", "random text", "merge branch"], "1.0.0")
    assert "- a" in out and "random text" not in out


def test_prepend_creates_title_when_missing():
    out = prepend_section(None, "## [1.0.0]\n\n### Features\n\n- a\n")
    assert out.startswith("# Changelog")
    assert "## [1.0.0]" in out


def test_prepend_keeps_old_entries_below():
    existing = "# Changelog\n\n## [1.0.0]\n\n### Features\n\n- old\n"
    out = prepend_section(existing, "## [1.1.0]\n\n### Features\n\n- new\n")
    assert out.index("## [1.1.0]") < out.index("## [1.0.0]")
    assert out.count("# Changelog") == 1
