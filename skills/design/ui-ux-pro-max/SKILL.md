---
name: ui-ux-pro-max
description: Design and review usable product interfaces against UI/UX best practice — usability heuristics, affordances, forms, the loading/empty/error/success/partial states, feedback, hierarchy, navigation, and accessibility. Use when designing or reviewing a screen, form, flow, or component; auditing a page's UX; fixing missing empty or error states, unconfirmed destructive actions, forms that lose data, keyboard or contrast gaps, or unclear primary actions.
---

Design or review an interface the way a usability expert does: judge it against the
user's task and how little the user must already know, not only whether the pixels are
tidy. Visual polish is the floor; the leverage is in visible status, honest affordances,
recoverable errors, complete states, and accessibility.

The full method — Nielsen's 10 heuristics, interaction and affordance patterns, form
design, the five system states, feedback and perceived performance, information hierarchy
and progressive disclosure, navigation, accessibility, failure modes, and a worked
example — lives in [references/ux-principles.md](references/ux-principles.md). Load it
before judging a screen.

## Steps

1. **Name the user and the task.** State who uses this screen and the one job it exists to
   complete (submit the form, find the setting, recover from the error). A review without
   the task checks usability against nothing. Done when the primary user and the single
   task are written in one sentence each.

2. **Run the heuristic pass.** Score the screen against the 10 heuristics in the
   reference, marking each as a pass or a violation with a severity. Done when all 10
   heuristics carry a verdict and every violation names the user task it endangers.

3. **Audit the system states.** Inventory the loading, empty, error, success, and partial
   state of every data-bearing view. Done when each of the five states carries a verdict
   of present or gap, with no data view left at success-only.

4. **Check forms, feedback, and hierarchy.** Verify persistent labels, inline validation,
   preserved input, a confirmation after every write, and one primary action per view.
   Done when each form field carries a visible label and a per-field error path, and each
   view names exactly one primary action.

5. **Run the accessibility checks.** Verify keyboard reach and order, a visible and
   managed focus ring, native semantics with ARIA only for the gaps, a 4.5:1 text contrast
   ratio, and no signal carried by color alone. Done when every interactive control
   activates from the keyboard and text clears the contrast threshold.

6. **Scan the failure modes and red flags.** Match the screen against the failure modes
   and the red-flag list in the reference — mystery-meat navigation, missing states,
   unconfirmed destructive actions, data-losing forms. Done when each red flag is marked
   present or absent.

7. **Rank and report against checkable criteria.** Label each finding blocker, major, or
   minor, tied to the principle it failed and the task it endangers, and pair it with the
   observable condition that closes it. Done when every finding carries a severity, a
   cause, and a verifiable fix condition.
