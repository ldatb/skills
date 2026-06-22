# The ambiguity rules

`skill-lint` is the deterministic reviewer for SKILL.md files. It replaces "have an
agent re-read the skill for ambiguity" with a check that runs identically every time.

The patterns, thresholds, and messages are defined in
[`tools/skill_lint/rules.yaml`](../../../../tools/skill_lint/rules.yaml) — the single
source of truth. This page explains *why* each rule exists; it deliberately does not
restate the patterns (that would be duplication that drifts).

## Rules

| ID | Name | Why it exists | The fix |
|----|------|---------------|---------|
| SK001–SK008 | frontmatter | The frontmatter is the invocation contract; a wrong `name`, missing `description`, or a model-invoked skill with no triggers fires unreliably | Match `name` to the folder; give a description; add triggers or set `disable-model-invocation` |
| SK010 | pronoun-ambiguity | A sentence opening with a bare pronoun ("It should…", "This causes…") has no anchored referent — exactly where resolution turns nondeterministic | Name the noun the pronoun stands for |
| SK020 | context-explosion | "for each / all / every / any" over an open set blows up the working set on a large project | Bound the scope, or pass it to a script that enumerates deterministically |
| SK030 | conditional-complexity | More than one conditional in a sentence is branching the agent follows only some of the time | One branch per step, or move the decision into a script |
| SK040 | destructive-operation | An inlined `rm -rf`, `DROP TABLE`, `git reset --hard` is a footgun the agent may fire | Call `skillkit.safe_remove` or another guarded helper |
| SK041 | vague-destructive | "clean up", "wipe", "start fresh" have a dangerously broad reading | State exactly what is removed and what is kept |
| SK050 | concurrency-hazard | A time-based filename collides under concurrent runs | `skillkit.unique_path` |
| SK060 | vague-imperative | "make sure", "as needed", "handle appropriately" have no checkable completion criterion | Replace with an observable condition |
| SK070 | skill-too-long | Length is a proxy for sprawl; an over-long SKILL.md hides what matters | Disclose reference material into linked files |
| SK080 | unresolved-marker | A `TODO` / `FIXME` left in a published skill is unfinished work shipped as done | Resolve it before commit |

## Severities and the gate

- **error** — always fails the build (`SK001`–`SK005`, `SK040`, `SK080`, …).
- **warning** — fails under `--strict`, which pre-commit and CI both pass.
- **info** — advisory only.

Run `skill-lint --strict skills/` (or `make lint`) before every commit.

## Suppression

When a skill must legitimately quote a banned construct — a doctrine page showing what
*not* to write — waive the rule narrowly:

- One line: append `<!-- skill-lint: allow SK040 -->`.
- A region: `<!-- skill-lint: disable SK040 -->` … `<!-- skill-lint: enable SK040 -->`.

Suppress the *narrowest* scope that works, and only with a reason. A suppression is a
debt; prefer rewriting the prose so the rule passes honestly.

## Extending the linter (Kaizen)

When you find an ambiguity the linter misses:

1. Add a rule to `rules.yaml` (data only — pattern, severity, message).
2. Add a fixture and an assertion in `tools/skill_lint/tests/test_linter.py`.
3. Run `make test`; the new case fails, then passes once the rule is right.

The linter only ever grows sharper. A defect caught once is caught forever.
