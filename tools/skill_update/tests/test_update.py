"""Version parsing and comparison are total and deterministic."""

from __future__ import annotations

from skill_update.core import is_newer, parse_version


def test_parse_variants():
    assert parse_version("v1.2.3") == (1, 2, 3)
    assert parse_version("1.2") == (1, 2, 0)
    assert parse_version("3") == (3, 0, 0)
    assert parse_version("not-a-version") is None


def test_is_newer():
    assert is_newer("1.2.0", "1.1.9")
    assert is_newer("v2.0.0", "1.9.9")
    assert not is_newer("1.0.0", "1.0.0")
    assert not is_newer("0.9.0", "1.0.0")


def test_is_newer_unparseable_is_false():
    assert not is_newer("garbage", "1.0.0")
    assert not is_newer("1.0.0", "garbage")
