---
name: polish
description: The final polish pass that turns "works" into "impeccable" — the last 5% a user feels but a spec never names. Use when a feature is functionally complete and needs a finishing pass, when the work feels rough or cheap, before a release or demo, or when the user asks to polish, refine, or tighten the details of a UI, flow, output, or screen.
---

The polish pass turns "works" into "impeccable". A finished feature still carries small
flaws no spec names — a stray pixel, a generic label, a missing focus ring, a blank
empty state. Each is forgivable alone; stacked, these cuts compound into a cheap feel.
This pass finds them deliberately and drives them to zero on the path the user walks.

Polish is the **last** step. Confirm the behavior is complete and the tests pass before
sweeping for cuts — a rough edge on unfinished work is not a paper cut, the work is
simply not done. Work the dimensions against
[the polish checklist](references/polish-checklist.md), one at a time, so attention is
forced onto the small.

## Steps

1. **Confirm readiness.** State that the feature is functionally complete and its tests
   pass. Readiness is confirmed when behavior is done and the suite is green; an
   unfinished feature exits here, because polish on incomplete work is premature.

2. **Establish the reference.** Locate the design system, style guide, or token
   definitions; absent one, name the convention visible in neighboring screens. This
   step is done when the correct spacing scale, color tokens, component set, and motion
   curves are named, so deviations can be measured rather than guessed.

3. **Walk the real path.** Use the feature as the audience does, on the slowest device
   and network the audience has. The walk is done when each point where the experience
   stutters is noted, before any inspector opens.

4. **Sweep every dimension.** Take the checklist sections one at a time — visual, copy,
   interaction, edge cases, consistency, accessibility. The sweep is done when each of
   the six sections has been worked against the screen and yields a verdict.

5. **Log each cut as a line item.** Record every finding with its location, the fix,
   and a **functional** or **cosmetic** label. Logging is done when each cut found sits
   in the list with its fix named, in the table format the checklist shows.

6. **Fix at the root.** Resolve each logged cut at its cause — patch the system token,
   swap to the shared component, or rework the flow — not at the single instance. This
   step is done when a fixed cut has been checked for the same cut elsewhere on the
   surface.

7. **Verify zero cuts.** Re-walk the user's path and re-run the suite. The pass is
   complete when the line-item list shows every cut resolved, no new cut appears on the
   re-walk, and the tests stay green.
