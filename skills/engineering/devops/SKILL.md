---
name: devops
description: Build and change infrastructure safely — validate, scan, plan, then apply behind review. Use when the user works on Terraform, Docker, Kubernetes, Ansible, CI/CD, or deployment.
---

Infrastructure changes are reviewed before they touch a live system. This skill runs the deterministic gates for the IaC stack, then routes any mutation through an approved plan.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Detect the stack.** Run `skill-gate --list` at the repo root. The output names the infra gates for Terraform, Docker, Kubernetes, or Ansible. Confirm the list matches the project.

2. **Validate and lint.** Run `skill-gate --category format`, then `--category lint`. A non-zero exit blocks progress; fix the definition, then rerun until each exits zero.

3. **Scan for misconfiguration.** Run `skill-gate --category sast`, then `--category sca`. A high or critical finding blocks the change until resolved.

4. **Plan, never apply blind.** Produce the change plan and read it (for example, a Terraform plan). A mutation reaches a live system only after a human approves the printed plan.

5. **Guard destruction.** A teardown or delete runs only against a named, non-production target with explicit approval. The approval and the target are recorded before the command runs.

6. **Ship.** Hand the approved plan to the pipeline. The change is done when the gates are green and the applied state matches the reviewed plan.
