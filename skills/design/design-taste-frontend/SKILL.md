---
name: design-taste-frontend
description: Raise the taste level of a frontend UI — judge whether it looks intentional or generic, then fix what reads as generic. Use when the user asks to make a UI look better, polished, premium, less like a template or bootstrap default; when a component or page "looks off / cheap / AI-generated"; when reviewing visual design, spacing, typography, color, or hierarchy; or before shipping a marketing page, landing page, dashboard, or app screen.
---

Taste is the judgment that separates a polished UI from a generic one, and a UI rarely fails on a single broken rule — a UI fails by accumulating small defaults nobody decided. Run this procedure to locate those defaults and replace each with a deliberate choice. The depth of the judgment lives in [cultivating-taste.md](references/cultivating-taste.md); read it before the first pass.

The root test, applied to every element: **does this look intentional, or does it look generic?** A generic element is one no human chose — a framework default, a round number nobody measured, a color straight from a palette. Taste is the sum of choices made on purpose.

## Steps

1. **Name the reference.** State one shipped product whose taste the UI should reach (Linear, Stripe, Vercel, Things), and name the single quality to borrow — density, restraint, type, motion. A pass without a target optimizes toward "fine," so the step is done once one named product and one named quality are written down.

2. **Audit against the markers of taste.** Walk the UI through the six markers in [cultivating-taste.md](references/cultivating-taste.md): one accent color, a real type scale, generous whitespace, aligned edges, consistent radii and borders, and no default-framework look. Record each marker as a pass or a specific defect with its element. The step is done when all six markers carry a verdict.

3. **Catch the anti-patterns.** Scan for the six taste-killers — gradient soup, emoji section headers, drop-shadow on everything, more than two font families, unmodified component-library defaults, and the generic-SaaS-template silhouette. List every hit with its location. The step is done when the scan reaches the last element and the hit list is closed.

4. **Rank defects by visual weight.** Order the recorded defects by how much each one cheapens the first impression: hierarchy and spacing outrank color, color outranks border-radius. Label each blocker, major, or minor. The step is done once every defect carries a rank and a severity.

5. **Raise one component end to end.** Take the highest-ranked component and apply the before/after method in [cultivating-taste.md](references/cultivating-taste.md): collapse the palette to one accent, snap spacing to a scale, set a type hierarchy, align every edge, remove decorative shadow. The step is done when the rebuilt component passes all six markers from step 2.

6. **Re-test intentional versus generic.** Put the revised UI beside the step-1 reference and ask the root test element by element. A surviving "generic" verdict reopens step 5 for that element. The step is done when no element reads as a default nobody chose.

7. **Verify against the checklist.** Confirm the closing checklist in [cultivating-taste.md](references/cultivating-taste.md): one accent color, one type scale of four-to-six sizes, spacing on a single scale, two font families at most, zero emoji headers, shadows only where elevation is real, every edge aligned to a grid. The work is done when each line of the checklist is checkably true.
