---
name: gpt-taste
description: Detect and remove generic AI "slop" from generated design and writing, pushing output toward distinctive, intentional, human-feeling work. Use when reviewing or fixing AI-generated UI, landing pages, marketing copy, or any draft that feels generic, templated, or machine-made — purple gradients, centered hero, three-card rows, emoji bullets, hedging prose, "in today's fast-paced world", "it's not just X, it's Y", default unthemed shadcn.
---

Generated design and writing regress to the training mean: competent, generic, and instantly machine-made. This skill detects that slop and replaces it with specificity, a point of view, and a real constraint. The depth bar lives in [references/anti-slop.md](references/anti-slop.md) — read it before judging, since the tells, the four de-slopping moves, and the failure modes are catalogued there.

Detect first, then fix. Slop is the default output, not a defect of craft, so the work is to supply the inputs the median lacked.

## Steps

1. **Name the artifact and its intent.** State what the piece is (UI, landing section, marketing copy) and the one thing it must communicate or do. A de-slop pass without intent strips character at random. This step ends with a one-sentence intent statement written down.

2. **Run the visual detection pass.** Score the design against the visual tells in [references/anti-slop.md](references/anti-slop.md): purple/indigo gradients, the centered two-button hero, gratuitous glassmorphism, uniform shadows, the three-card feature row, emoji bullets, and stock-default shadcn. This step ends with each tell marked present or absent.

3. **Run the prose detection pass.** Score the copy against the prose tells: hedging, the "in today's fast-paced world" opener, listicle padding, em-dash overuse, the "it's not just X, it's Y" frame, and rule-of-three filler. This step ends with each prose tell marked present or absent.

4. **Locate the missing inputs.** For the tells marked present, name what the median lacked: a concrete detail, a stated opinion, a real constraint, or a reference to diverge from. A tell is slop because an input was absent, so this step ends with every present tell paired to the input it needs.

5. **Apply the four de-slop moves.** Inject concrete details, take a point of view, impose a real constraint, and name an anti-reference, fixing the structure before the surface. This step ends with a revised artifact in which no present tell from steps 2–3 survives.

6. **Guard against the de-slop failure modes.** Check the revision against the failure modes in [references/anti-slop.md](references/anti-slop.md): quirk for its own sake, specificity theater (fabricated facts), over-correction past useful convention, and de-slopped words on a still-generic skeleton. This step ends with each failure mode confirmed absent.

7. **Verify against the red-flags checklist.** Walk the revised artifact through the red-flags checklist in [references/anti-slop.md](references/anti-slop.md). The skill is done when the checklist shows zero yes answers and the intent from step 1 still holds.
