# Determinism: why, and how

## The problem

An agent is a stochastic system asked to follow a process written in human language.
Human language is saturated with ambiguity, so the same instruction can produce a
different process on different runs. The quality of the agent does not fix this — the
*language* is the core problem. Two runs of "clean up the old files and make sure
there are no collisions" can mean *check-then-create*, *delete-everything-first*, or
*remove the directory and recreate it*. All three satisfy the sentence.

## The strategy: move work from stochastic to deterministic

Wherever a task can be expressed as a rule, encode the rule and let a deterministic
tool enforce it. This is the same move a compiler makes over a style guide: instead
of asking a reviewer to remember a hundred conventions, a linter checks them, every
time, identically.

LLMs are *excellent at writing* deterministic tools and terrible at *being* one. So
use the model to author the linter, the script, the schema, the small DSL — then run
that artifact deterministically forever after. You pay the model once, at authoring
time, and get free, identical enforcement on every run after. Cheaper, faster, fewer
tokens, no drift.

### The determinism ladder

1. **Script / existing tool.** If a script can produce the output, the agent should
   call it, not reproduce it. `skill-new` writes a valid skill skeleton; the agent
   does not freehand the frontmatter.
2. **Validator.** If correctness can be checked, gate on the check. `skill-lint`
   decides whether a skill is conformant — not the agent's judgment.
3. **Primitive.** If the operation is a known hazard (unique naming, atomic write,
   deletion), call a `skillkit` primitive that removes the dangerous interpretation.
4. **Model.** Only the irreducibly creative or context-specific remainder goes to the
   model — and even then, its output is fed back through a validator where possible.

## Worked examples

### Collision-free file creation

"Create issue files named by timestamp; make sure there are no collisions" invites
the agent to *delete colliding files*. The deterministic fix removes the choice:

```python
from skillkit import unique_path
path = unique_path("issues", prefix="issue-", suffix=".md")  # kernel guarantees uniqueness
```

`unique_path` uses an atomic `O_CREAT | O_EXCL` create, so it is correct even when 50
copies run concurrently. The agent never reasons about collisions.

### Destruction without the footgun

An agent told "you cannot use `rm -rf`" will find another path to the same outcome —
deleting the directory and recreating it, for instance. Banning a *command* does not
ban the *capability*. The deterministic fix is a guarded primitive whose dangerous
behavior is impossible by construction:

```python
from skillkit import safe_remove
safe_remove(path, root="issues")  # refuses anything outside root, refuses root, never recurses
```

### Concurrency

"Create a file" is a concurrency hazard the moment two runs overlap. The linter flags
time-based naming (SK050) and points at `unique_path`, which is safe to run in
parallel.

## The discipline

A skill is not finished when it works once. It is finished when `skill-lint --strict`
is green, its scripts have tests, and the dangerous interpretations of its prose have
been designed out. Determinism is not a constraint on the work — it *is* the work.
