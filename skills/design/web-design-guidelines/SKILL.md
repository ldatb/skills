---
name: web-design-guidelines
description: Make a web UI look professionally designed via an opinionated system for spacing, type, color, hierarchy, layout, depth, motion, and accessibility — in the spirit of Refactoring UI and the Vercel design guidelines. Use when building or restyling a landing page, dashboard, or app screen; when a design "looks off / amateur / cramped" but the cause is unclear; when reviewing a hero, pricing table, form, or component for polish; or when picking a spacing scale, type scale, or palette.
---

Designs read as amateur for a small set of nameable reasons: spacing off any scale, too many typefaces and colors, weak hierarchy propped up by borders, low contrast, and everything centered. This skill replaces taste-by-vibes with a checkable system. Treat each rule as a default to follow unless a stated reason overrides it.

The full ruleset, failure modes, red flags, and a worked before/after live in [references/web-design-rules.md](references/web-design-rules.md). Load that reference before applying or reviewing.

## Steps

1. **Name the target and read the ruleset.** State the surface under design (hero, pricing, form, dashboard) and its single primary action, then read [references/web-design-rules.md](references/web-design-rules.md). Done when the surface, its one primary action, and the ruleset are all in hand.

2. **Lock the spacing and type scales.** Adopt one 8pt-based spacing scale (4, 8, 12, 16, 24, 32, 48, 64) and one modular type scale (per the reference), capped at two typefaces. Done when every margin, padding, gap, and font-size in the design maps to a named step on those two scales, with zero off-scale values.

3. **Restrain the palette and verify contrast.** Reduce to one neutral ramp plus one accent plus semantic success/warning/danger, then check body text and UI text against their backgrounds. Done when total hues are within the reference budget and every text-on-background pair measures at WCAG AA or higher (4.5:1 body, 3:1 large text).

4. **Build hierarchy with size, weight, color, and space — not borders.** Rank elements by importance and express that rank through type size, font weight, text color, and surrounding whitespace, demoting secondary text via lighter weight or muted color. Done when the primary action is the most prominent element and no separation relies on a border that whitespace or a background tint could carry instead.

5. **Set layout, density, and responsive behavior.** Constrain body copy to a 45–75 character measure, design the small viewport first, and define breakpoints per the reference. Done when line length sits in range, the layout holds at 360px wide, and each breakpoint reflows without a horizontal scrollbar.

6. **Apply depth and motion sparingly.** Use one soft shadow tier for raised surfaces and reserve motion for state changes and feedback, keeping transitions in the 150–300ms band and honoring reduced-motion preferences. Done when shadows come from the single defined tier, every animation signals a real state change, and a reduced-motion setting disables non-essential movement.

7. **Run the polish checklist.** Verify the design against the reference checklist: all spacing on the scale, contrast at AA or higher, two typefaces or fewer, hierarchy without border-soup, body measure 45–75 characters, mobile layout intact at 360px, one shadow tier, purposeful motion only, and keyboard-visible focus on every interactive element. Done when each checklist line passes or carries a written justified exception.
