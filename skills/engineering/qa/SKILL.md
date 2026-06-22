---
name: qa
description: Verify quality against acceptance criteria with layered tests and the test gate. Use when the user wants to test, write a test plan, check coverage, or verify a release.
---

Quality is defined before it is measured. This skill turns acceptance criteria into layered tests, then gates on them.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Define acceptance criteria.** Write the observable conditions that mean the feature works. Each criterion is specific enough to pass or fail without judgment.

2. **Layer the tests.** Cover each criterion at the lowest sufficient level: unit for logic, integration for boundaries, end-to-end for the critical path. A criterion without a test is a gap to record.

3. **Run the suite.** Run `skill-gate --category test`. A failing test blocks the release; fix the code, then rerun until the suite is green.

4. **Check coverage.** Measure coverage of the changed code. A criterion left uncovered is reported as a gap, not waved through.

5. **Report.** Write the result per criterion: covered and passing, or a named gap. The check is done when every criterion has a verdict.
