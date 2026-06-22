"""skill-gate — deterministic engineering gates for a project's stack.

One registry (gates.yaml) maps each stack to its ordered quality gates: format,
lint, types, sast, sca, secrets, test. Every engineering skill calls this runner
instead of re-describing tool commands in prose, so the commands live in exactly
one place (single source of truth) and run identically every time.
"""

from __future__ import annotations

__version__ = "0.1.0"
