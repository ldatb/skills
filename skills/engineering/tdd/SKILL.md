---
name: tdd
description: Build features and fix bugs test-first — red, green, refactor — with the loop enforced by the test gate. Use when the user wants to add a feature, fix a bug, or change behavior under tests.
---

Write the test before the code. The loop is red, then green, then refactor — and the loop is not optional.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Red.** Write one failing test that states the desired behavior. Run `skill-gate --category test`. The test fails for the stated reason before any implementation exists; a test that passes now tests nothing.

2. **Green.** Write the minimum code that makes the test pass. Run `skill-gate --category test` again. The suite is green before you add anything more.

3. **Refactor.** Improve the code without changing behavior. Run `skill-gate --category test` once more. The suite stays green; a red suite reverts the refactor.

4. **Harden.** Run `skill-gate --category lint`, then `--category types`. Both exit zero before the change is done.

5. **Repeat.** Take the next behavior and return to step 1. The feature is complete when every stated behavior has a green test.
