"""Link discovery and resolution behave deterministically."""

from __future__ import annotations

from skill_docs.cli import main
from skill_docs.core import check_file, find_links, is_local


def test_find_links():
    links = find_links("see [a](x.md) and ![img](y.png)")
    assert (1, "x.md") in links and (1, "y.png") in links


def test_is_local():
    assert is_local("x.md")
    assert not is_local("https://example.com")
    assert not is_local("#anchor")
    assert not is_local("mailto:a@b.c")


def test_check_file_flags_broken(tmp_path):
    (tmp_path / "exists.md").write_text("ok")
    doc = tmp_path / "doc.md"
    doc.write_text("[good](exists.md)\n[bad](missing.md)\n[ext](https://x.com)\n[anchor](#top)\n")
    broken = check_file(doc)
    assert [b.target for b in broken] == ["missing.md"]


def test_check_file_anchor_on_existing_is_ok(tmp_path):
    (tmp_path / "exists.md").write_text("ok")
    doc = tmp_path / "doc.md"
    doc.write_text("[sec](exists.md#section)\n")
    assert check_file(doc) == []


def test_cli_exit_codes(tmp_path):
    (tmp_path / "exists.md").write_text("ok")
    good = tmp_path / "good.md"
    good.write_text("[a](exists.md)\n")
    assert main([str(good)]) == 0
    bad = tmp_path / "bad.md"
    bad.write_text("[a](nope.md)\n")
    assert main([str(bad)]) == 1
