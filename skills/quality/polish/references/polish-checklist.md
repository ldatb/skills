# Polish checklist

The polish pass turns "works" into "impeccable" — the last 5% that a user feels but
a spec never names. The feature already functions; the gaps left are small, and small
gaps are the whole subject here. This reference holds the doctrine, the checklist, the
failure modes, and a worked example.

Polish is the **last** step, never the first. A rough corner on unfinished work is not
a paper cut; the work is simply not done. Polish a feature once the behavior is
complete and the tests pass.

## The thousand paper cuts

No single rough edge sinks a product. A 13px gap beside every 12px gap, a button that
reads "Submit" next to one that reads "Save changes", a spinner that never resolves on
a slow network, an empty state that shows a blank rectangle — each is forgivable alone.
Stacked, the cuts compound into a verdict the user cannot articulate: the thing feels
*cheap*. Cheapness is the sum of defects too small to file a bug against.

The cuts compound because the user reads them as one signal. A reader who hits three
inconsistencies stops trusting the fourth screen before seeing it. The cost is not
additive but multiplicative: each cut lowers the benefit of the doubt the next element
receives. Impeccable is the absence of that accumulated doubt — the state where nothing
on the surface contradicts the care underneath.

Two consequences follow. First, the bar is *zero* visible cuts on the path the user
walks, not "few". Second, a single cut left visible undermines the polish spent
elsewhere, so consistent mid quality beats one perfect corner beside three rough ones.

## How to run the pass deliberately

Polish fails most often by being done *vibe-first* — opening the screen, fixing
whatever the eye lands on, declaring victory. The eye anchors on the largest element
and skips the cuts. Run the pass against the checklist below instead, dimension by
dimension, so attention is forced onto the small.

1. **Establish the reference.** Find the design system, style guide, or token
   definitions. The system names the correct spacing scale, the color tokens, the
   component library, the motion curves. Absent a system, the reference is the
   convention already visible in neighboring screens. Polish without a reference is
   decoration on top of drift.

2. **Walk the real path.** Use the feature as the user does, on the slowest device and
   network the audience has. Note where the experience stutters before opening any
   inspector. Effective flow beats decorative shine; a beautiful screen that fights the
   user is not polished.

3. **Sweep each dimension.** Take the checklist sections one at a time — visual, copy,
   interaction, edge cases, consistency, accessibility. A focused sweep on one
   dimension catches cuts a general glance skips.

4. **Log every cut as a line item.** Write each finding down with its location and the
   fix. An unwritten cut is a cut that ships. The worked example below shows the format.

5. **Classify and triage.** Mark each cut **functional** (breaks, blocks, or confuses)
   or **cosmetic** (looks off, does not impede). On a tight clock, functional cuts ship
   first; cosmetic cuts can follow. Quality stays even across the surface either way.

6. **Fix the root, not the instance.** A 13px gap on one card is a typo; the same wrong
   gap on twenty cards is a missing token. Patch the system value, swap to the shared
   component, or rework the flow — the fix differs by cause.

## The checklist

### Visual — alignment, spacing, optical adjustment

- **Alignment.** Elements line up to a shared grid; edges and baselines agree across a row.
- **Spacing consistency.** Gaps draw from the spacing scale; a lone 13px gap beside 12px gaps is drift.
- **Optical adjustment.** A glyph or icon sits optically centered, not metrically centered — a triangular play icon nudges right of mathematical center to look centered.
- **Responsive parity.** Spacing and alignment hold at every named breakpoint, not the design width alone.
- **No layout shift.** Content keeps its position after load; a late-loading image reserves its box rather than shoving text.

Red flags: random off-scale pixel values; elements that "feel off" when squinted at; a layout that only lines up at one viewport.

### Copy — microcopy, errors, empty states, labels

- **Button labels.** A label names the action the button performs ("Save changes"), not a generic verb ("Submit", "OK").
- **Error messages.** An error states what went wrong and the recovery path, in plain language, never a raw code or a blamed user.
- **Empty states.** A first-run or no-data view orients the user and offers the next action, never a blank rectangle.
- **Microcopy.** Helper text, tooltips, and placeholders carry the product voice and earn their space; no restated label.
- **Mechanics.** No typo, no stray double space; capitalization and punctuation follow one rule across labels.

Red flags: "An error occurred"; placeholder text mistaken for a value; a tooltip restating its own label.

### Interaction — states, transitions, loading

- **Hover.** An interactive element gives subtle feedback on pointer-over (color, elevation, or cursor).
- **Focus.** A keyboard-focused element shows a visible indicator with sufficient contrast; the indicator is never removed without a replacement.
- **Active.** A press registers immediately with a distinct pressed appearance.
- **Disabled.** A non-interactive control reads as unavailable and explains why on hover when the reason is non-obvious.
- **Loading.** An async action shows progress within ~100ms; a long wait shows a skeleton over a spinner where layout is known.
- **Transitions.** A state change eases over 150–300ms with an ease-out curve; motion respects `prefers-reduced-motion`.

Red flags: a missing focus ring; a button with no pressed state; a spinner with no resolution on failure; bounce or elastic easing.

### Edge cases — long text, zero/one/many, slow network, errors

- **Long text.** A long name, title, or value wraps or truncates with a tooltip, never overflowing its container or breaking the layout.
- **Zero / one / many.** The view holds for an empty list, a single item, and a thousand; grammar agrees ("1 item" vs "2 items").
- **Slow network.** The screen stays coherent during a slow or stalled request, with progress shown and a timeout path.
- **Failure.** A failed request surfaces a recoverable error, never a frozen UI or a silent swallow.
- **Boundary data.** A zero value, a negative number, a missing field, and an unexpected type each render without breaking.

Red flags: a happy-path-only demo; "0 items" pluralized wrong; a layout that explodes on a 200-character name.

### Consistency — terminology, iconography, formatting

- **Terminology.** One concept carries one name across the surface; a "Workspace" here is not a "Project" three screens away.
- **Iconography.** Icons share one family, weight, and optical size; no mixed line-and-fill set.
- **Formatting.** Dates, numbers, currency, and units follow one format throughout.
- **Capitalization.** Title Case versus sentence case is applied by one rule, not per author.
- **Pattern reuse.** A comparable action takes the established shape (modal vs route, inline vs separate, save-on-blur vs explicit submit), not a fresh one.

Red flags: two names for one thing; an icon from a foreign set; "Jan 3" beside "03/01/2026".

### Accessibility — focus order, labels

- **Focus order.** Tab order follows reading order; no trap, no skipped control, no off-screen stop.
- **Labels.** Every input, icon-button, and image carries a programmatic label or alt text a screen reader can announce.
- **Contrast.** Text and meaningful UI meet WCAG AA contrast against their background.
- **Semantics.** Native elements or correct ARIA roles convey structure; a clickable `div` is a button in markup, not in name only.
- **Touch targets.** An interactive target is at least 44×44px on touch.

Red flags: an icon-button with no accessible name; a focus order that jumps around the page; gray text on a colored fill below AA.

## Failure modes

- **Shipping rough edges.** Declaring done at "works", leaving the cuts for the user to find. The fix is the deliberate pass above — the cuts are invisible to the builder precisely because the builder built them.

- **Polishing the wrong thing.** Spending the budget on the element that caught the eye while the user's actual path stays rough. Walk the real flow first; fix what the user hits, not what the builder notices.

- **Gold-plating.** Adding animation, flourish, or configuration nobody asked for, past the point of diminishing return. Polish removes defects and adds no scope. A custom easing curve on a screen still missing its empty state is gold-plating. Stop when the cuts are gone, not when invention runs out.

- **Decoration on drift.** Styling a screen that does not match the system's flow or naming. Surface shine on a misshapen flow is wasted; align the shape first.

- **Perfecting one corner.** One flawless screen beside three rough ones reads worse than three even ones, because the contrast advertises the roughness. Hold quality level across the surface.

- **Polishing the incomplete.** Sweating pixels on a feature whose behavior is unfinished. Finish the function and pass the tests, then polish.

## Red flags (pass-level)

- No design-system or convention reference was consulted before polishing.
- The pass was driven by the eye, with no checklist and no written line items.
- Only the happy path and the design-width viewport were exercised.
- Found cuts were fixed at the instance, with no check for the same cut elsewhere.
- New scope (animation, options, flourish) appeared under the name of polish.
- "Done" was declared with no list of cuts found and no list of cuts fixed.

## Worked example — a settings screen

A single "Notification settings" screen, swept against the checklist. Twelve paper cuts
found, each with its fix.

| # | Dimension | Paper cut | Fix |
|---|---|---|---|
| 1 | Visual | Section gaps alternate 16px / 20px / 16px down the page | Snap all section gaps to the 16px scale token |
| 2 | Visual | The toggle column is 2px out of alignment with the label column | Align both columns to the same grid line |
| 3 | Visual | The bell icon looks low beside its label (metrically centered) | Nudge the icon up 1px for optical centering |
| 4 | Copy | Primary button reads "Submit" | Relabel to "Save changes" |
| 5 | Copy | Save failure shows "Error: 500" | Replace with "Could not save. Check your connection and retry." plus a Retry action |
| 6 | Copy | Empty state for "Muted channels" is a blank box | Add a one-line orientation and an "Add a channel" action |
| 7 | Interaction | Toggles have no focus ring under keyboard navigation | Restore a visible focus indicator at AA contrast |
| 8 | Interaction | Save shows no progress on a slow network | Show an inline spinner and disable the button while the request is in flight |
| 9 | Edge case | A long channel name overflows its row | Truncate with an ellipsis and a full-name tooltip |
| 10 | Edge case | The counter renders "1 channels" | Pluralize by count: "1 channel" / "2 channels" |
| 11 | Consistency | The header says "Alerts", the body says "Notifications" | Pick one term and apply it across the screen |
| 12 | Accessibility | The icon-only "Edit" button has no accessible name | Add an `aria-label="Edit channel"` |

None of the twelve would block a release on its own. Together they are the difference
between a screen that feels shipped and one that feels considered. The pass found them
because it swept each dimension on purpose; the eye, left alone, would have fixed the
button label and missed the other eleven.
