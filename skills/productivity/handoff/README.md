# handoff

> Write a handoff document so another agent or person resumes the work with zero context loss — goal, current state, what is done, what remains with next concrete actions, files touched, decisions, gotchas, and how to verify. Use when the user is pausing work, ending a session, switching agents, going off-shift, hitting a context limit, or asks to write a handoff, handover, transfer notes, or a resume-from-here document.

**Model-invoked** — the agent runs it automatically when your request matches the triggers below. You can also invoke it by name.

## When to use

- is pausing work
- ending a session
- switching agents
- going off-shift
- hitting a context limit
- asks to write a handoff
- handover
- transfer notes
- a resume-from-here document

## What it does

1. Stamp the document structure with the script.
2. Fill the Summary with the goal.
3. Fill Current state against the goal.
4. Fill What's done, then make each item under What's left a concrete action.
5. Fill the run, risk, file, and contact sections.
6. Confirm resumability against the failure modes.

## Scripts

- `scripts/handoff.sh`

## Learn more

- [SKILL.md](SKILL.md) — the full procedure the agent follows.

---

*Generated from SKILL.md by `skill-readme`. Run `skill-readme` to refresh; do not edit by hand.*
