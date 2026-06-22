---
name: code-review
description: Review a change deterministically — run every gate, then a fixed checklist — and report findings by severity. Use when the user asks to review code, a diff, or a pull request.
---

Review starts with the tools, not opinions. Run the deterministic gates first; spend human judgment only on what a tool cannot decide.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Scope the change.** Identify the changed files from the diff under review. Confirm the scope with the author before reviewing beyond it.

2. **Run the gates.** Run `skill-gate --strict` at the repo root. Record every failing gate as a finding; a green gate needs no comment.

3. **Apply the checklist.** Review the changed files against [the review checklist](references/checklist.md): correctness, security, tests, readability. Each item produces a finding or a pass.

4. **Rank findings.** Label each finding blocker, major, or minor. A blocker stops the merge; a minor is advisory.

5. **Report.** Write the findings grouped by severity, each with a file and line. The review is done when every changed file has been accounted for.
