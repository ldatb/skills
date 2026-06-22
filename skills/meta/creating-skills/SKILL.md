---
name: creating-skills
description: Author a new skill the deterministic way — scaffold, write to the doctrine, lint, verify. Use when the user wants to create, add, or scaffold a skill in this repository.
---

Create a skill that is born conformant. The process is deterministic end to end: a scaffolder writes a valid skeleton, and the linter gates the result.

Read [the foundation doctrine](../foundation/SKILL.md) first; this skill assumes those rules.

## Steps

1. **Scaffold.** Run `make new-skill CATEGORY=<category> NAME=<name>` (or `skill-new --category <category> --name <name>`). The command writes a lint-clean `skills/<category>/<name>/SKILL.md` and registers the skill in the plugin manifest. Confirm the file exists before continuing.

2. **Choose invocation.** A skill the agent must fire on its own is model-invoked; pass `--invocation model` and give the description trigger phrasing. A skill only you type stays user-invoked, the default. Decide once, before writing the body.

3. **Write the body.** Replace the scaffold steps with the real process. Each step ends on a checkable condition. Prefer a script over freehand judgment. Push reference material into linked files so the top stays legible.

4. **Lint.** Run `make lint`. The build stays red until `skill-lint --strict` reports zero findings. Fix the skill, not the linter — a genuinely wrong rule gets a new test case and a `rules.yaml` change instead (Kaizen).

5. **Verify scripts.** A skill that ships a script ships a test for it. Run `make test`; the suite passes before the skill is done.

6. **Confirm registration.** Check that `./skills/<category>/<name>` appears in `.claude-plugin/plugin.json`. The scaffolder adds the entry; verify by reading the file rather than assuming it (Genchi Genbutsu).
