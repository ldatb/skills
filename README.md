# Agent Skills

**Deterministic Claude skills, built to a manufacturing standard.**

[![ci](https://github.com/ldatb/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/ldatb/skills/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A skill exists to wring **determinism** out of a stochastic system: the agent takes
the *same process* every run. This repository treats that as an engineering problem,
not a prompting one, and solves it the way a factory solves defects, by building
quality in rather than inspecting it afterward.

## The thesis

An agent follows a process written in human language, and human language is full of
ambiguity. "Clean up the old files and make sure there are no collisions" can mean
three different things, including *delete everything first*. The agent's quality does
not fix this; the **language** is the problem.

So we move work out of the model and into deterministic tools:

- **Scripts** do the work the model would otherwise improvise.
- **Linters** enforce the rules the model would otherwise forget.
- **Guarded primitives** make the dangerous interpretation *impossible*, not merely
  discouraged.

You use the model once, to *author* these tools, then run them deterministically
forever. Cheaper, faster, and identical every time.

This is **Poka-yoke** (mistake-proofing) and **Jidoka** (stop the line on a defect)
applied to agent skills. The full doctrine lives in
[`skills/meta/foundation`](skills/meta/foundation/SKILL.md).

## Quickstart

```bash
git clone https://github.com/ldatb/skills.git
cd skills
make install        # venv + toolchain + pre-commit hooks
make lint           # skill-lint --strict over every skill
make test           # the toolchain's own test suite
```

Skills are standard `SKILL.md` files under `skills/`, organized by domain. The
`.claude-plugin/plugin.json` manifest makes the set installable by the Claude Code
plugin system.

## How it works

### The determinism ladder

Climb until a rung holds, then stop — the model is the last resort, not the first:

1. **Script / existing tool** can do it → call it.
2. **Validator** can check it → gate on it.
3. **Primitive** exists for the hazard → use `skillkit`.
4. **Model** gets only the irreducibly creative remainder.

### skill-lint — a deterministic reviewer for skills

Instead of asking an agent to re-read a skill for ambiguity (slow, nondeterministic,
expensive), a linter checks it identically every time. It flags unanchored pronouns,
unbounded "for-each" scope (context explosion), compound conditionals, inlined
destructive commands, collision-prone file creation, and uncheckable completion
criteria. Rules are **data** in
[`tools/skill_lint/rules.yaml`](tools/skill_lint/rules.yaml) — adding a case is a
data edit plus a test, never a rewrite (**Kaizen**).

```bash
skill-lint --strict skills/      # the gate; runs in pre-commit and CI
```

### skillkit — guarded primitives

Skills call these instead of describing file operations in prose:

| Primitive | Guarantee |
| --------- | --------- |
| `unique_path` | Collision-free name, atomic `O_CREAT\|O_EXCL`, safe under concurrency |
| `atomic_write` | A reader never sees a half-written file |
| `safe_remove` | Refuses anything outside its root, refuses the root, never recurses |

### skill-new — born conformant

```bash
make new-skill CATEGORY=engineering NAME=my-skill
```

Generates a lint-clean `SKILL.md` and registers it in the manifest, so a malformed
skill cannot be created by hand (**Poka-yoke** at authoring time).

## Repository layout

```bash
skills/                 # the skills, by domain
  meta/                 # the foundation + how to author skills
    foundation/         # the determinism doctrine every skill inherits
    creating-skills/    # the authoring procedure
  engineering/          # (next) secure SDLC: lint/SCA/Semgrep gates, TDD
tools/                  # the deterministic toolchain (Python)
  skill_lint/           # the linter + its rule DSL + tests
  skill_new/            # the scaffolder
  skillkit/             # guarded primitives
.claude-plugin/         # plugin.json manifest
.github/workflows/      # CI: the determinism gate, tests, ruff, Semgrep
```

## Categories

Skills are filed by domain. The taxonomy grows as skills land — no empty folders.

| Domain | What lives here |
| ------ | --------------- |
| `meta` | The foundation and skill-authoring skills |
| `engineering` | Secure SDLC, TDD, linting/SCA gates, code review |
| `obsidian` | Script-driven second-brain / vault operations |
| `personal` | Life ops, routines, decision logs |
| `marketing` · `sales` · `social` | Brand, outreach, content engines |

## Authoring a skill

Read [the foundation doctrine](skills/meta/foundation/SKILL.md), then follow
[`creating-skills`](skills/meta/creating-skills/SKILL.md): scaffold → write to the
doctrine → `make lint` green → `make test` green → commit. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Quality gates

Every change passes the same gates locally (pre-commit) and in CI (**Jidoka** — a
violation is a red build, not a warning):

- `skill-lint --strict` — the determinism gate
- `pytest` — the toolchain test suite
- `ruff` — Python lint/format
- `semgrep` — static analysis (SCA) on the toolchain

## License

[MIT](LICENSE).
