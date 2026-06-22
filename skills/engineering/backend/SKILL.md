---
name: backend
description: Build and change backend services test-first, behind the security and quality gates. Use when the user builds or changes an API, server, or backend service.
---

Backend code ships behind the same gates as everything else, with the contract and the tests written first.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Define the contract.** State the endpoint or function signature: inputs, outputs, errors, and the authorization required. The contract is written before the implementation.

2. **Test-first.** Follow [tdd](../tdd/SKILL.md): a failing test per stated behavior, then the minimum code to pass.

3. **Validate input at the boundary.** Reject malformed or unauthorized requests before any work happens. Each input is checked against the contract.

4. **Run the gates.** Run `skill-gate --category lint`, `--category types`, then `--category sast`. Each exits zero before the change proceeds.

5. **Audit dependencies.** Run `skill-gate --category sca`. A high or critical advisory blocks the change.

6. **Verify.** Run `skill-gate --category test`. The change is done when the suite is green and every contract behavior has a test.
