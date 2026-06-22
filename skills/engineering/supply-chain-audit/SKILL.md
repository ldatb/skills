---
name: supply-chain-audit
description: Audit dependencies for known vulnerabilities, generate an SBOM, and check supply-chain risk. Use when the user wants to scan for CVEs, audit dependencies, produce an SBOM, or assess supply-chain risk.
---

Treat every dependency as untrusted until scanned. This skill runs the SCA and secrets gates, then produces an attestation of what is in the build.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Inventory.** Detect the stacks with `skill-gate --list`. The dependency manifests for those stacks are the audit scope. Confirm the scope before scanning.

2. **Scan dependencies.** Run `skill-gate --category sca`. Record each known vulnerability with its severity and affected package; a critical or high finding blocks the release.

3. **Scan for secrets.** Run `skill-gate --category secrets`. A leaked credential is a blocker, and the credential is rotated before anything else proceeds.

4. **Generate the SBOM.** Produce a CycloneDX SBOM for the build (for example, `syft . -o cyclonedx-json`). The SBOM lists every component and version.

5. **Attest.** Write the report: the SBOM path, the vulnerability counts by severity, and the secrets result. The audit is done when every stack in the inventory has a scan result.
