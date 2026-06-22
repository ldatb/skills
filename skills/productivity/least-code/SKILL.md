---
name: least-code
description: Write the least code that fully works — climb the subtraction ladder before adding anything. Use when the user wants to simplify, cut scope, avoid over-engineering, or review a change for unnecessary complexity.
---

The best code is the code never written. Climb the ladder and stop at the first rung that holds; reach for new code only after nothing simpler works.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## The ladder

Stop at the first rung that holds:

1. **Does this need to exist?** A speculative need is skipped, and the reason is stated in one line.
2. **Does the standard library cover it?** Use it.
3. **Does a native platform feature cover it?** A built-in beats a dependency.
4. **Does an installed dependency solve it?** Use it before adding a new one.
5. **Can it be one line?** Write the one line.
6. **The last rung** is the minimum code that works.

## Never simplify away

Validation at trust boundaries, error handling that prevents data loss, security controls, and accessibility basics stay in. Brevity never removes them.

## The check

Non-trivial logic leaves one runnable check behind: the smallest test that fails if the logic breaks. A deliberate shortcut carries a comment that names the ceiling and the upgrade path.
