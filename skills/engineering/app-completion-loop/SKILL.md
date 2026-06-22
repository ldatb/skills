---
name: app-completion-loop
description: Drive an application to done in checkpointed iterations — plan, build test-first, gate, repeat. Use when the user wants to finish an app, work through a backlog, or build to acceptance criteria.
---

Build to a definition of done, one checkpointed iteration at a time. The loop pauses at each phase boundary for approval, so progress stays deterministic and reviewable.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Define done.** Write the acceptance criteria as observable conditions. The loop ends when every criterion passes its gate.

2. **Plan the next slice.** Choose the smallest slice that moves a criterion toward done. State the slice and pause for approval before building.

3. **Build test-first.** Follow [tdd](../tdd/SKILL.md) for the slice: a failing test, then the minimum code to pass.

4. **Gate.** Run `skill-gate --strict`. A failing gate keeps the slice open; fix the code, then rerun until the gate is green.

5. **Checkpoint.** Report the slice result and the criteria still open. Pause for approval to continue.

6. **Loop or finish.** Return to step 2 while a criterion remains open. The app is done when every acceptance criterion passes the gates.
