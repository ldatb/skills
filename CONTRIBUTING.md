# Contributing

The bar is determinism: a skill must take the same process every run. Everything below
serves that. Read [the foundation doctrine](skills/meta/foundation/SKILL.md) before
your first contribution.

## Setup

```bash
make install     # venv, toolchain (editable), and pre-commit hooks
```

## Adding a skill

Follow [`creating-skills`](skills/meta/creating-skills/SKILL.md):

1. **Scaffold** — `make new-skill CATEGORY=<domain> NAME=<name>`. This writes a
   lint-clean `SKILL.md` and registers it in `.claude-plugin/plugin.json`.
2. **Choose invocation** — user-invoked by default; `--invocation model` (with trigger
   phrasing in the description) only when the agent must fire it on its own.
3. **Write the body** — each step ends on a checkable condition; prefer a script over
   freehand judgment; disclose reference material into linked files.
4. **Lint** — `make lint` must report zero findings under `--strict`.
5. **Test** — a skill that ships a script ships a test; `make test` must pass.

## Changing the linter

The linter only ever grows sharper (**Kaizen**). To add a rule:

1. Add it to `tools/skill_lint/rules.yaml` (data only — pattern, severity, message).
2. Add a fixture and an assertion in `tools/skill_lint/tests/test_linter.py`.
3. `make test` — the new case fails, then passes once the rule is right.

Fix the skill, not the linter — unless a rule is genuinely wrong, in which case the
fix is a test plus a rule change, never a silent loosening.

## Before you open a PR

```bash
make lint     # skill-lint --strict
make test     # toolchain tests
make sca      # Semgrep (matches CI)
make format   # ruff
```

All four run in CI and block the merge. Green locally means green there.

## Commit messages

Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`,
`perf:`, `ci:`. One logical change per commit.

## Principles, briefly

- **Poka-yoke** — prefer making a mistake impossible over warning against it.
- **Kanso** — the shortest skill that works wins; prune no-op lines.
- **Genchi Genbutsu** — verify by running the gate and reading the output, not by
  assuming.
- **Shokunin** — you own the green build. "It mostly works" is not done.
