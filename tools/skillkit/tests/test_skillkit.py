"""Assertions that the deterministic primitives actually hold their guarantees."""

from __future__ import annotations

import os

import pytest

from skillkit import atomic_write, is_within, safe_remove, unique_id, unique_path


def test_unique_id_distinct_and_prefixed():
    ids = {unique_id() for _ in range(1000)}
    assert len(ids) == 1000
    assert unique_id("issue-").startswith("issue-")


def test_unique_path_never_collides(tmp_path):
    paths = {unique_path(tmp_path, prefix="n", suffix=".md") for _ in range(500)}
    assert len(paths) == 500
    for p in paths:
        assert p.exists()
        assert p.parent == tmp_path
        assert p.name.startswith("n") and p.name.endswith(".md")


def test_atomic_write_roundtrip_and_creates_parents(tmp_path):
    target = tmp_path / "nested" / "deep" / "file.txt"
    atomic_write(target, "hello")
    assert target.read_text() == "hello"
    atomic_write(target, "replaced")
    assert target.read_text() == "replaced"
    # no leftover temp files
    assert [p.name for p in target.parent.iterdir()] == ["file.txt"]


def test_atomic_write_bytes(tmp_path):
    target = tmp_path / "b.bin"
    atomic_write(target, b"\x00\x01\x02")
    assert target.read_bytes() == b"\x00\x01\x02"


def test_is_within(tmp_path):
    assert is_within(tmp_path, tmp_path / "a" / "b")
    assert is_within(tmp_path, tmp_path)
    assert not is_within(tmp_path / "a", tmp_path)


def test_safe_remove_file(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("data")
    assert safe_remove(f, root=tmp_path) is True
    assert not f.exists()


def test_safe_remove_missing_returns_false(tmp_path):
    assert safe_remove(tmp_path / "ghost", root=tmp_path) is False


def test_safe_remove_refuses_root(tmp_path):
    with pytest.raises(ValueError):
        safe_remove(tmp_path, root=tmp_path)


def test_safe_remove_refuses_outside_root(tmp_path):
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("x")
    try:
        with pytest.raises(ValueError):
            safe_remove(outside, root=tmp_path)
        assert outside.exists()
    finally:
        outside.unlink()


def test_safe_remove_refuses_nonempty_dir(tmp_path):
    d = tmp_path / "full"
    d.mkdir()
    (d / "child").write_text("x")
    with pytest.raises(OSError):
        safe_remove(d, root=tmp_path)
    assert d.exists()


def test_safe_remove_empty_dir(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    assert safe_remove(d, root=tmp_path) is True
    assert not d.exists()


def test_safe_remove_symlink_unlinks_link_not_target(tmp_path):
    target = tmp_path / "real.txt"
    target.write_text("keep")
    link = tmp_path / "link.txt"
    os.symlink(target, link)
    assert safe_remove(link, root=tmp_path) is True
    assert not link.exists()
    assert target.exists()
