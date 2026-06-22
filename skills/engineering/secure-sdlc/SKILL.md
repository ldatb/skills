---
name: secure-sdlc
description: Orchestrate every deterministic quality and security gate before a change ships. Use when the user wants to ship securely, run all gates, harden a change, or verify a build before merge.
---

Ship a change only after every deterministic gate is green. This skill orchestrates the gates; the commands live in `skill-gate`, not here, so each run is identical.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Detect the stack.** Run `skill-gate --list` at the repo root. The output names every gate that applies to the detected stacks. Confirm the list matches the project before continuing.

2. **Run the quality gates.** Run `skill-gate --category format`, then `--category lint`, then `--category types`. A non-zero exit blocks the pipeline; fix the code, then rerun until each exits zero.

3. **Run the security gates.** Run `skill-gate --category sast`, then `--category sca`, then `--category secrets`. A finding here blocks the merge — triage dependency and CVE detail with [supply-chain-audit](../supply-chain-audit/SKILL.md).

4. **Run the tests.** Run `skill-gate --category test`. The suite passes before the change is shippable.

5. **Gate the merge.** Run `skill-gate --strict` for the final pass. A missing tool now counts as a failure, so the attestation covers the whole stack. Green here is the definition of done (Jidoka).
