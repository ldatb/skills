# CLAUDE.md — working in this repository

This repo builds **deterministic** Claude skills. The root virtue is predictability:
the same process every run. Honor it.

## Before authoring or editing a skill

1. Read [`skills/meta/foundation/SKILL.md`](skills/meta/foundation/SKILL.md) — the
   doctrine every skill inherits.
2. Create new skills with the scaffolder, never by hand:
   `make new-skill CATEGORY=<domain> NAME=<name>`.

## Non-negotiable rules (enforced by `skill-lint`)

- Anchored references — no sentence-initial bare pronoun.
- Bounded scope — no unbounded "for-each / all / every / any".
- Shallow branching — one conditional per sentence.
- Guarded destruction — never inline `rm -rf` and the like; call `skillkit.safe_remove`.
- Collision-free creation — `skillkit.unique_path`, never a hand-rolled timestamp.
- Checkable completion — no "make sure" / "as needed"; end on an observable condition.

## The deterministic toolchain

- `skill-lint --strict skills/` — the gate. Runs in pre-commit and CI.
- `skill-new` — scaffolds a lint-clean, registered skill.
- `skillkit` — `unique_path`, `atomic_write`, `safe_remove`. Use these instead of
  describing file operations in prose.

## Before you finish

`make lint && make test` must be green. A red gate is not done (**Jidoka**). Verify by
running the gate and reading the output, not by assuming (**Genchi Genbutsu**).

## Where things live

- `skills/<domain>/<name>/SKILL.md` — the skills.
- `tools/skill_lint/rules.yaml` — the single source of truth for lint rules.
- `tools/` — the Python toolchain and its tests.
