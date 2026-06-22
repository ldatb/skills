# Glossary

The leading words this repository thinks in. A leading word recruits a concept the
model already holds, so one token anchors a whole region of behavior.

## Determinism & predictability

**Predictability** — the agent takes the same *process* every run. The root virtue;
every rule serves it. Distinct from reproducible *output* (often impossible) — what
we control is the path, not the destination.

**Determinism ladder** — the ordered preference: script → validator → primitive →
model. Climb until a rung holds; the model is the last resort.

**Ambiguity** — the enemy. Any phrasing an LLM can resolve more than one way. The
linter exists to find and kill it.

**Context explosion** — what happens when a skill ranges over an open set ("for each
file…") on a large project: the working set blows past what fits, and behavior
degrades. Bounded scope prevents it.

## Skill anatomy

**Leading word** — a compact, pretrained concept the agent thinks with while running
a skill. Repeated use accumulates a distributed definition.

**Progressive disclosure** — pushing reference material out of SKILL.md into linked
files, reached by a pointer, so the top stays legible.

**Completion criterion** — the observable condition that tells the agent a step is
done. Checkable, and where it matters, exhaustive.

**Single source of truth** — one authoritative place for each meaning, so a change is
a one-place edit. `rules.yaml` is the source of truth for lint rules; the docs point
to it rather than restating the patterns.

**Suppression** — an inline directive (`<!-- skill-lint: allow SK0xx -->`) that waives
a rule on one line, or a `disable` / `enable` pair across a region. Used when a skill
must legitimately quote a banned construct.

## Japanese quality principles

**Poka-yoke** (ポカヨケ) — mistake-proofing. Make the wrong action structurally
impossible, not merely discouraged.

**Jidoka** (自働化) — autonomation: stop the line the instant a defect appears. The
linter failing the build is the andon cord.

**Genchi Genbutsu** (現地現物) — go and see. Verify against real, observed output.

**Kaizen** (改善) — continuous improvement. Each new defect becomes a permanent
check.

**Kanso** (簡素) — simplicity through elimination of clutter.

**Shokunin** (職人) — the craftsman's commitment to mastery and ownership of quality.

**Hansei** (反省) — honest reflection on what went wrong, without excuse.

**Muda** (無駄) — waste. Work that adds no value: a no-op line, a redundant agent
turn, rework caused by ambiguity.

**Andon** (アンドン) — the signal that halts the line. Here, a red lint or CI run.
