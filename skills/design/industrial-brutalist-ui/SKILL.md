---
name: industrial-brutalist-ui
description: Apply the industrial / neo-brutalist UI aesthetic well — exposed structure, high contrast, heavy mono type, hard edges, offset shadows — distinctive without becoming unusable. Use when building or restyling a UI in a raw, brutalist, or industrial look; for a dev tool, indie product, portfolio, or statement brand; when a brutalist design reads as broken, illegible, or low-contrast; or when judging whether the raw aesthetic fits a given product at all.
---

Neo-brutalism exposes the grid, leans on monospace and heavy type, refuses gradients and
soft shadows, and treats friction as a deliberate signal. Done well, the look is confident
and distinctive. Done badly, the same moves read as a broken stylesheet or an excuse for
no design at all. The dividing line is contrast, legibility, and keyboard support — this
skill keeps the raw look while holding that line.

The full system — principles, building blocks, fit and no-fit, accessibility, failure
modes, red flags, and a worked card-and-button example — lives in
[references/brutalist-system.md](references/brutalist-system.md). Load that reference
before applying or judging the aesthetic.

## Steps

1. **Name the surface and confirm fit.** State the surface under design (card, form,
   dashboard, landing page) and its audience, then check that audience against the fit and
   no-fit lists in the reference. Done when the surface is named, and a one-line verdict
   records that the aesthetic suits this audience or that a calmer system should win.

2. **Read the system and lock the palette.** Read [the reference](references/brutalist-system.md),
   then fix one paper, one ink, and one or two loud accents as named tokens. Done when the
   palette is a token set of three-to-four colours with zero gradients defined.

3. **Set the structural type and grid.** Choose a monospace or heavy grotesk face, an
   oversized heading scale, and a column grid with hard alignment and wide gutters. Done
   when the type face, heading scale, and grid columns are named values, and headings sit
   at least two steps above body size.

4. **Render the raw blocks.** Build panels and controls as solid-fill rectangles with
   thick borders (2–4px), hard or near-zero corner radius, and solid un-blurred offset
   shadows. Done when no element carries a gradient, a blurred shadow, or a soft pillowy
   radius.

5. **Verify contrast at AA.** Compute the contrast ratio of every text-on-background pair,
   including text on a loud accent. Done when each body pair measures 4.5:1 or higher and
   each large-text and meaningful-border pair measures 3:1 or higher.

6. **Wire keyboard and touch support.** Give each control a `:focus-visible` state
   distinct from its hover state, a 44x44px minimum target, and a second non-colour signal
   on each accent-marked state. Done when keyboard focus is visibly distinct from hover,
   targets clear 44px, and no state relies on colour alone.

7. **Run the red-flag pass.** Check the design against the red-flag list in the reference:
   sub-AA contrast excused as style, missing or hover-equal focus, accent-only state,
   sub-44px targets, monospace body at length, "raw" standing in for no design, and a
   trust-sensitive flow wearing the look against its goal. Done when every red flag is
   absent or carries a written justified exception.
