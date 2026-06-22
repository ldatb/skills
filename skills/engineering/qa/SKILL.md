---
name: qa
description: Verify quality against acceptance criteria with a layered test strategy and the test gate. Use when the user wants to test, write a test plan, check coverage, or verify a release.
---

Quality is defined before it is measured. Turn acceptance criteria into a layered test strategy, then gate on it. A test that cannot fail proves nothing — each test earns its place by catching a real defect.

## Steps

1. **Define acceptance criteria.** Write the observable conditions that mean the feature works. Each criterion is specific enough to pass or fail without judgment.

2. **Choose the layer.** Place each criterion at the lowest sufficient level using [the test strategy](references/test-strategy.md): unit for logic, integration for boundaries, end-to-end for the critical path. A criterion without a test is a recorded gap.

3. **Write failing tests.** Each test fails before the behavior exists and asserts behavior, not implementation. Cover the failure paths, not only the happy path.

4. **Run the suite.** Run `skill-gate --category test`. A red suite blocks the release; fix the code, then rerun until it is green.

5. **Judge coverage.** Measure coverage of the changed code. Coverage is a floor, not a goal — an uncovered criterion is a gap, and a covered-but-unasserted line is a false comfort.

6. **Report.** Write the verdict per criterion: covered and passing, or a named gap with its risk. The check is done when every criterion has a verdict.
