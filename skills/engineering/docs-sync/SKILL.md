---
name: docs-sync
description: Keep documentation in sync with code — detect broken references and update docs when code changes. Use when the user changes code, renames files, or asks to update or verify the docs.
---

Docs drift the moment code moves. This skill catches the drift deterministically, then updates the prose a tool cannot write.

Read [the foundation doctrine](../../meta/foundation/SKILL.md) first.

## Steps

1. **Detect drift.** Run `skill-docs` at the repo root. The output lists every Markdown link or file reference that no longer resolves. A non-zero exit blocks the change.

2. **Repair references.** Fix each broken link to point at the moved or renamed target. Rerun `skill-docs` until it exits zero.

3. **Update the prose.** For the code that changed, update the matching docs: the README, the public API notes, and the affected guides. The doc states the new behavior, not the old.

4. **Regenerate API docs.** Run the stack's documentation generator where one exists (for example, typedoc or godoc). The generated reference matches the current signatures.

5. **Verify.** Run `skill-docs` once more, then [changelog-gen](../changelog-gen/SKILL.md). The change is done when links resolve and the changelog records the change.
