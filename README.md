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

## Install

Tell any Claude Code agent with this repo available: **"install ldatb skills"** — the
[`setup`](skills/meta/setup/SKILL.md) skill runs the install. Or do it by hand (requires
[uv](https://docs.astral.sh/uv/)):

```bash
# 1. the CLIs the skills call (skill-lint, skill-gate, skill-changelog, skill-docs, skill-update)
git clone https://github.com/ldatb/skills.git && cd skills
./scripts/install.sh                       # uv tool install from the clone; re-run to update

# 2. the skills, as a Claude Code plugin
/plugin marketplace add ldatb/skills
/plugin install ldatb-skills@ldatb-skills
```

`skill-update` reports when a newer tagged release exists.

## Develop

```bash
make install        # uv sync + pre-commit hooks
make lint           # skill-lint --strict over every skill
make docs           # skill-docs — every Markdown link resolves
make test           # the toolchain's own test suite
```

Skills are standard `SKILL.md` files under `skills/`, organized by domain.

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
  meta/                 # foundation, creating-skills, setup, cavecrew
  engineering/          # secure-sdlc, tdd, code-review, supply-chain-audit, engineering,
                        # git-guardrails, autoguardrails, ralph, software-architecture, ...
  quality/              # verification-before-completion, polish, overdrive, full-output-enforcement
  marketing/            # copywriting, ad-creative, cold-email, social-content, revops, ...
  design/               # web-design-guidelines, ui-ux-pro-max, brandkit, gpt-taste, ...
  documents/            # pptx, pdf, docx, xlsx (beautiful, deterministic generation)
  cloud/                # aws-toolkit, azure-toolkit, gcp-toolkit, cloud-best-practices
  obsidian/             # obsidian-vault (vault compiler), second-brain-crud, ralph-vault
  management/           # project-management, client-satisfaction, employee-management
  productivity/         # grill-me, least-code, caveman, handoff, teach, simple
  social/               # social-media-viral
tools/                  # the deterministic toolchain (Python): skill_lint, skill_new,
                        # skill_gate, skill_changelog, skill_docs, skill_update, skillkit
scripts/                # install.sh, git-commit.sh
.claude-plugin/         # marketplace.json + plugin.json
.github/workflows/      # CI: determinism gate, docs, tests, ruff, Semgrep
```

## Categories

62 skills across 11 domains, every one lint-gated. The taxonomy grows as skills land — no empty folders.

| Domain | What lives here |
| ------ | --------------- |
| `meta` | Foundation, skill-authoring, install/setup, the cavecrew subagent protocol |
| `engineering` | Secure SDLC, TDD, code review, supply-chain, architecture, git/auto guardrails, autonomous loops |
| `quality` | Verification-before-completion, polish, overdrive, full-output enforcement |
| `marketing` | Copy, ads, cold email, social content, sales enablement, RevOps, PR, psychology |
| `design` | Web/UI-UX guidelines, design taste, anti-AI-slop, brandkit, brutalist UI |
| `documents` | Beautiful deterministic pptx, pdf, docx, xlsx generation |
| `cloud` | AWS / Azure / GCP toolkits + cross-cloud SOC2 best practices |
| `obsidian` | Source-backed vault compiler + fast second-brain CRUD |
| `management` | Project management, client satisfaction, people management |
| `productivity` | grill-me, least-code, caveman, handoff, teach, simple |
| `social` | Viral research for Instagram + X |

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
