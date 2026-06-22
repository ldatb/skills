---
name: frontend
description: Build and change UI behind type, lint, accessibility, and test gates. Use when the user builds or changes a frontend, UI, or web client.
---

UI ships accessible, typed, and tested. This skill runs the frontend gates and holds accessibility as a first-class requirement.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Build the component.** Implement the smallest component that meets the requirement. Reuse an existing primitive over a new one.

2. **Make it accessible.** Give interactive elements roles, labels, and keyboard support. Each interactive element is reachable and operable without a mouse.

3. **Type and lint.** Run `skill-gate --category types`, then `--category lint`. Each exits zero before the change proceeds.

4. **Test behavior.** Follow [tdd](../tdd/SKILL.md): a test per user-visible behavior, asserting what the user sees rather than the implementation.

5. **Scan dependencies.** Run `skill-gate --category sca`. A high or critical advisory blocks the change.

6. **Verify.** Run `skill-gate --category test`. The change is done when the suite is green and the component is keyboard-operable.
