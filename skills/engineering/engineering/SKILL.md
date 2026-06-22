---
name: engineering
description: Build and change application software — design judged before code, built test-first, shipped behind the gates. Use when the user implements a feature, edits app code, builds an API or UI, or asks how to build something.
---

Build software that fits the system and delivers the requirement. Judge the design before writing code, build it test-first, and ship it behind the gates. The hard part is rarely the code — it is choosing the right seam and proving the change does what was asked.

## Steps

1. **State the requirement.** Write what the change must deliver and the acceptance criteria that decide done. Code measured against nothing cannot be reviewed.

2. **Design the seam.** Name the boundary the change lives behind: the interface, the data shape, the dependency direction. Check the design against [engineering practices](references/engineering-practices.md) before writing code; a wrong seam is expensive to move later.

3. **Build test-first.** Follow [tdd](../tdd/SKILL.md): a failing test per stated behavior, then the minimum code that passes.

4. **Validate at the boundary.** Reject malformed or unauthorized input before any work runs. Untrusted data is checked at the edge, not deep in the call stack.

5. **Finish the user-facing edges.** For a UI change, cover the loading, empty, and error states and the accessibility checklist in the practices. For an API change, cover the error contract, pagination, and idempotency.

6. **Run the gates.** Run `skill-gate --strict`. A red gate blocks; fix the code, then rerun until it is green.

7. **Verify against the requirement.** Confirm each acceptance criterion holds against the running change. The work is done when every criterion passes and the gates are green.
