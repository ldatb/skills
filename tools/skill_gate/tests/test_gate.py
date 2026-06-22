"""Detection, filtering, and execution behavior for skill-gate.

Execution is tested with the always-present ``true`` / ``false`` utilities and a
deliberately-missing tool, so the suite needs no real linters installed.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from skill_gate.cli import main
from skill_gate.core import Status, build_gates, detect_stacks, load_gates, run_gate

REAL_GATES = load_gates()


def write_gates(tmp_path: Path) -> Path:
    path = tmp_path / "gates.yaml"
    path.write_text(
        textwrap.dedent(
            """
            version: 1
            stacks:
              dummy:
                markers: [dummy.marker]
                gates:
                  - {id: ok, category: test, cmd: ["true"]}
                  - {id: nope, category: lint, cmd: ["false"]}
                  - {id: absent, category: sca, cmd: ["definitely-not-a-real-tool-xyz"], install: "n/a"}
            """
        )
    )
    return path


# --- detection ------------------------------------------------------------
def test_detects_python(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    assert "python" in detect_stacks(tmp_path, REAL_GATES)


def test_detects_go(tmp_path):
    (tmp_path / "go.mod").write_text("module x\n")
    assert "go" in detect_stacks(tmp_path, REAL_GATES)


def test_detects_terraform_by_glob(tmp_path):
    (tmp_path / "main.tf").write_text('resource "null_resource" "x" {}\n')
    assert "terraform" in detect_stacks(tmp_path, REAL_GATES)


def test_no_stack(tmp_path):
    assert detect_stacks(tmp_path, REAL_GATES) == []


# --- filtering ------------------------------------------------------------
def test_build_gates_category_filter():
    gates = build_gates(["python"], REAL_GATES, category="sca")
    assert gates
    assert all(g.category == "sca" for g in gates)


# --- execution ------------------------------------------------------------
def test_run_pass(tmp_path):
    gates = build_gates(["dummy"], load_gates(write_gates(tmp_path)))
    ok = next(g for g in gates if g.id == "ok")
    assert run_gate(ok, tmp_path).status is Status.PASS


def test_run_fail(tmp_path):
    gates = build_gates(["dummy"], load_gates(write_gates(tmp_path)))
    nope = next(g for g in gates if g.id == "nope")
    assert run_gate(nope, tmp_path).status is Status.FAIL


def test_missing_tool_skipped_then_failed_under_strict(tmp_path):
    gates = build_gates(["dummy"], load_gates(write_gates(tmp_path)))
    absent = next(g for g in gates if g.id == "absent")
    assert run_gate(absent, tmp_path).status is Status.SKIPPED
    assert run_gate(absent, tmp_path, strict=True).status is Status.FAIL


# --- cli exit codes -------------------------------------------------------
def test_cli_fails_when_a_gate_fails(tmp_path):
    gpath = write_gates(tmp_path)
    (tmp_path / "dummy.marker").write_text("")
    assert main([str(tmp_path), "--gates", str(gpath)]) == 1


def test_cli_passes_with_only_passing_gates(tmp_path):
    gpath = write_gates(tmp_path)
    (tmp_path / "dummy.marker").write_text("")
    assert main([str(tmp_path), "--gates", str(gpath), "--category", "test"]) == 0


def test_cli_list_does_not_execute(tmp_path):
    gpath = write_gates(tmp_path)
    (tmp_path / "dummy.marker").write_text("")
    assert main([str(tmp_path), "--gates", str(gpath), "--list"]) == 0
