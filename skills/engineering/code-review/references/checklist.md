# Review checklist

The deterministic gates (`skill-gate --strict`) already cover formatting, lint, types,
SAST, SCA, secrets, and tests. This checklist covers only what a tool cannot decide.
Each item yields a finding (with file and line) or an explicit pass.

## Correctness

- Does the change do what the diff/PR description claims?
- Are edge cases handled: empty input, boundary values, large input, concurrent calls?
- Are errors handled at every level, with no silently swallowed exceptions?
- Is the logic free of off-by-one, sign, and ordering mistakes?

## Security

- Is all external input validated at the trust boundary?
- Are secrets absent from the diff (no keys, tokens, passwords)?
- Are queries parameterized and output encoded (no injection/XSS)?
- Is authorization checked on every new endpoint or action?

## Tests

- Does every new behavior have a test that fails without the change?
- Do the tests assert behavior, not implementation detail?
- Are the failure paths tested, not just the happy path?

## Readability & design

- Are names accurate and the control flow shallow (no deep nesting)?
- Is the change the smallest one that solves the problem (no speculative abstraction)?
- Is data immutable where practical, with no hidden mutation?
- Are public functions documented where intent is non-obvious?

## Severity

- **blocker** — incorrect, insecure, or untested behavior; stops the merge.
- **major** — a real defect or risk that should be fixed before release.
- **minor** — advisory: style, naming, or a non-blocking improvement.
