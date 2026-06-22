# Brand system

A brand kit is the contract a product keeps with the eye and ear of its
audience. The contract holds when the same intent renders the same way on the
site, the app, a slide, and a social post — and breaks the moment a second blue,
a second heading font, or a second voice appears. Coherence is the deliverable;
the tokens, the rules, and the worked example below exist to make incoherence
hard to ship.

This reference works on two jobs: **defining** a kit from nothing, and
**auditing** a kit that already exists. The depth is the same for both. A
founder's brand carries the product, the pitch, and the personal channel at
once, so a drifted palette or a voice that swings from playful to legalese costs
trust across every surface.

---

## 1. Brand foundations

The visual layer renders a strategy. A logo and a palette chosen before the
strategy is named are decoration, and decoration drifts because nothing anchors
it.

### Positioning

State the single claim the brand owns, in one sentence: **for [audience] who
[need], [brand] is the [category] that [differentiator], unlike [alternative].**
A positioning statement that fits two competitors equally well has named no
position. The differentiator must be a thing a rival cannot also say.

### Personality

Pick three to five traits, and pin each against its opposite so the trait
constrains a real choice: *confident, not arrogant*; *warm, not soft*; *precise,
not clinical*. A trait with no stated opposite permits everything and therefore
guides nothing. The traits drive the type, the color temperature, and the
imagery later in this reference — name them first so those choices inherit a
reason.

### Voice and tone

**Voice** is the constant — the personality rendered in words. **Tone** is the
voice bent to a context: an onboarding screen, an error, a launch tweet, a
churned-user email each ask for a different bend of the same voice.

Specify voice on a small set of axes the writer can apply without guessing:

| Axis | Pin one end |
|---|---|
| Formality | Casual ↔ Formal |
| Energy | Calm ↔ Energetic |
| Warmth | Neutral ↔ Warm |
| Humor | Dry ↔ Playful |
| Authority | Peer ↔ Expert |

Give the writer a lexicon, not adjectives alone: five words the brand says,
five it never says, and a rewrite of one real sentence before and after. A voice
defined only as "friendly and professional" produces nothing repeatable, because
the next writer reads those two words differently.

**Foundations check:** positioning excludes at least one named competitor; every
personality trait carries an opposite; voice is pinned on every axis with a
say / never-say list.

---

## 2. Visual identity

### Logo usage

The logo is the most-reproduced asset and the easiest to corrupt. Specify the
primary lockup, the contexts each variant serves, and the rules that keep every
reproduction faithful:

- **Variants** — primary, a monochrome version, a reversed (light-on-dark)
  version, and an icon-only mark for avatars and favicons. Tie each variant to
  the surface it serves so the choice is mechanical.
- **Clear space** — the minimum margin, expressed as a fraction of the mark
  (such as *half the cap height on every side*), so the rule scales with size.
- **Minimum size** — the smallest width in pixels and in print, below which the
  mark loses legibility.
- **Misuse, banned explicitly** — no stretch, no recolor outside the palette, no
  added shadow or outline, no rotation, no swapped background that breaks
  contrast, no busy photo behind the mark.

A logo section without an explicit misuse list invites every misuse, because the
absence reads as permission.

### Color system

A color system is **roles**, not a swatch grid. A swatch grid says *here are
nine blues* and leaves the next person to guess which one a primary button takes.
A role system says *this token is the action color* and removes the guess.

Name every color by the job it does, give it a value, and pair it with a
foreground that meets the WCAG AA contrast ratio (**4.5:1** for body text, **3:1**
for large text and UI boundaries):

| Role | Token | Job | Paired foreground |
|---|---|---|---|
| Primary / brand | `color.brand` | Identity, primary actions | `color.on-brand` (≥4.5:1) |
| Accent | `color.accent` | Highlights, secondary CTAs | `color.on-accent` (≥4.5:1) |
| Neutral scale | `color.neutral.50…900` | Text, surfaces, borders | adjacent steps ≥4.5:1 for text |
| Background | `color.bg` | Page and surface base | `color.fg` (≥4.5:1) |
| Success / Warning / Danger | `color.success` / `.warning` / `.danger` | Status, feedback | `color.on-{status}` (≥4.5:1) |

Rules that keep the system coherent:

- Each role gets **one** value per theme. A second hand-picked brand blue is the
  first crack in coherence.
- Every text-bearing pairing names its AA ratio. A color with no paired
  foreground is an accessibility bug shipped as a design choice.
- A dark theme defines the same roles, not new colors. The roles stay constant;
  the values flip.

### Type system

Type carries more of the brand's voice than the palette does, and a runaway font
list is the most common source of drift. Constrain it to a scale.

- **Families** — one or two, with roles: a display or heading family, a body
  family, and an optional mono for code or data. Three families is usually one
  too many.
- **Scale** — a fixed ramp on a ratio (1.250 major third is a safe default):
  `font.size.xs` through `font.size.4xl`. Sizes outside the ramp are the leak to
  watch for in an audit.
- **Weights** — name the two or three weights in use (such as 400 / 600 / 700);
  the rest are off-limits.
- **Line height and tracking** — bind to the size token, tighter on display,
  looser on body, so the rhythm is built in rather than re-decided per screen.

### Spacing, radius, elevation

The quiet tokens — the ones a founder skips and a designer never does. A spacing
scale off a base unit makes every layout rhythmically consistent without anyone
measuring.

- **Spacing** — a base unit (4px or 8px) and a ramp of multiples:
  `space.1 … space.12`. Padding and gaps draw from the ramp, never from arbitrary
  pixels.
- **Radius** — a small set: `radius.sm / md / lg / full`, mapped to component
  classes (inputs, cards, pills) so corners stay consistent.
- **Elevation** — a shadow ramp `elevation.0 … elevation.4` tied to z-layers
  (base, card, dropdown, modal, toast), so depth reads as a system rather than a
  pile of one-off shadows.

### Iconography

- **One library, one style** — outline or filled, a single stroke width, a
  single grid. A second icon style is as loud a break as a second font.
- **Sizes from the token scale** — `icon.sm / md / lg`, aligned to the spacing
  ramp so icons sit on the same rhythm as everything else.
- **Color by role** — icons inherit `color.fg` or a status role, never a
  one-off hex.

### Imagery direction

- **Subject and treatment** — what the brand photographs or illustrates, and the
  treatment (duotone, full color, flat illustration) that keeps a mixed set
  looking like one set.
- **Mood, tied to personality** — the imagery inherits the traits from §1. A
  *warm, precise* brand does not ship cold stock photography.
- **A do / don't pair** — one on-brand image beside one off-brand image teaches
  the boundary faster than a paragraph.

**Visual-identity check:** logo carries every variant plus a misuse list; every
color has a role and an AA-rated foreground; type, spacing, radius, and elevation
each resolve to a named scale; icons share one library; imagery names subject,
treatment, and mood.

---

## 3. Naming the tokens

Tokens turn a brand from a PDF into something a codebase enforces. A name a
designer and an engineer read the same way is the difference between a system and
a suggestion.

Name by **role, not by value**. `color.brand` survives a rebrand from blue to
green; `color.blue-500` becomes a lie the day the brand changes. Use a
consistent structure — `category.role.variant` — and keep it flat enough to read:

```
color.brand              color.on-brand
color.neutral.700        space.4
font.family.body         font.size.lg
radius.md                elevation.2
```

Layer the tokens so a value lives in exactly one place:

1. **Primitive** — the raw value: `palette.indigo.600 = #4f46e5`.
2. **Semantic** — the role pointing at a primitive: `color.brand = palette.indigo.600`.
3. **Component** *(optional)* — `button.bg = color.brand`.

Surfaces consume **semantic** tokens; a screen referencing a primitive directly
is the leak to flag. One source of truth (a `tokens.json` or a theme file)
generates the CSS variables, the design-tool styles, and the docs, so the three
never diverge.

**Token check:** every token names a role, not a raw value; primitive, semantic,
and component layers are separated; one file is the single source.

---

## 4. Usage do's and don'ts

| Do | Don't |
|---|---|
| Reference a semantic token for color | Paste a raw hex into a component |
| Draw spacing from the ramp | Type an arbitrary pixel value |
| Pick the logo variant the surface dictates | Recolor or restretch the mark |
| Bend tone to context, hold voice constant | Swap voice between channels |
| Add a need to the system, then a token | Add a one-off value beside the system |
| Check contrast before shipping a pairing | Ship a color without a foreground |

The pattern under every row: extend the system, never bypass it. A one-off is
not a small exception — it is the precedent that makes the next one-off defensible.

---

## 5. Consistency across surfaces

The kit only matters where surfaces meet. The same `color.brand`, the same
heading family, and the same voice render on each surface; what changes is
density and format, not identity.

| Surface | Inherits | Adapts |
|---|---|---|
| Marketing site | Full palette, type scale, voice | Generous spacing, hero imagery |
| Product / app | Roles, tokens, component radius | Denser scale, more neutrals, state colors |
| Social | Brand + accent, logo, voice | Square crops, larger type, icon-only mark |
| Decks / sales | Palette, type, imagery | Slide grid, presenter-scale type |
| Email | Logo, brand color, voice | Inline-safe styles, conservative fonts |

**Consistency check:** one token set drives every surface; per-surface
adaptation changes density and format only, never the identity values.

---

## 6. Failure modes

Each failure has a tell an audit catches and a token-level fix.

- **Inconsistent palette** — two brand blues, three "almost grey" greys. *Tell:*
  raw hex values scattered across screens. *Fix:* collapse to one semantic role
  per job; delete the strays.
- **No tokens** — values typed inline everywhere. *Tell:* a color change means a
  find-and-replace across the codebase. *Fix:* extract primitives, then point
  semantic tokens at them.
- **Logo misuse** — stretched, recolored, low-contrast on a busy photo. *Tell:*
  the mark looks different in two places. *Fix:* publish variants plus an
  explicit misuse list; ship a favicon-grade icon variant.
- **Voice drift** — playful onboarding, legalese errors, a stiff changelog.
  *Tell:* two screens read as two companies. *Fix:* a say / never-say lexicon and
  one before/after rewrite per surface.
- **Contrast failures** — light grey on white, brand color on brand color.
  *Tell:* text under 4.5:1 against its background. *Fix:* pair every role with an
  AA-rated foreground; re-pick the values that fail.
- **Scale leakage** — font sizes and paddings off the ramp. *Tell:* a `13px`
  beside the `xs / sm / md` scale. *Fix:* snap every value to the nearest token;
  remove the off-ramp ones.

---

## Red flags

Signals that a kit is decoration, not a system:

- A swatch page with no roles — colors named by hue, not by job.
- A color with no paired foreground anywhere in the doc.
- More than two heading fonts, or font sizes that do not sit on a named ramp.
- Spacing values that are not multiples of the base unit.
- A logo section with variants but no misuse list.
- Voice described only as adjectives, with no say / never-say lexicon.
- Raw hex or pixel values inside component styles.
- A second theme that introduces new colors instead of reusing the roles.
- Identity that shifts between the site, the app, and social.

---

## Worked mini brand kit — "Lumen" (founder analytics product)

A compact, coherent kit. Positioning, personality, and voice on top; the token
set below.

**Positioning:** for solo founders who drown in dashboards, Lumen is the
analytics tool that surfaces the one metric that moved, unlike suites that show
everything at once.

**Personality:** *clear, not clever · calm, not flashy · expert, not academic.*

**Voice axes:** Casual-leaning · Calm · Warm · Dry · Peer-expert.
**Says:** clear, signal, moved, focus, today. **Never says:** synergy,
leverage (as a verb), unlock, revolutionary, robust.

**Voice in context:**

| Surface | Tone bend | Example line |
|---|---|---|
| Onboarding | Warm, encouraging | "Connect one source. We'll find the signal." |
| Error | Calm, plain | "That source timed out. Retrying now." |
| Launch post | Dry, confident | "One metric. The one that moved. That's Lumen." |

**Design tokens:**

| Token | Value | Role | AA pair |
|---|---|---|---|
| `color.brand` | `#3b5bdb` | Primary actions, identity | `color.on-brand` `#ffffff` (5.7:1) |
| `color.accent` | `#0ca678` | Positive deltas, highlights | `color.on-accent` `#ffffff` (3.1:1, large only) |
| `color.bg` | `#ffffff` | Page base | `color.fg` `#1a1b1e` (17.2:1) |
| `color.fg` | `#1a1b1e` | Body text | on `color.bg` (17.2:1) |
| `color.neutral.500` | `#868e96` | Muted text, borders | on `#ffffff` (3.3:1, large/UI only) |
| `color.danger` | `#e03131` | Negative deltas, errors | `color.on-danger` `#ffffff` (4.5:1) |
| `font.family.display` | `Söhne` | Headings | — |
| `font.family.body` | `Inter` | Body, UI | — |
| `font.size.base` | `16px` | Body baseline | — |
| `font.size.scale` | `1.250` | Major-third ramp | — |
| `space.base` | `8px` | Spacing unit | — |
| `radius.md` | `8px` | Cards, inputs | — |
| `radius.full` | `9999px` | Pills, avatars | — |
| `elevation.2` | `0 4px 12px rgba(0,0,0,.08)` | Dropdowns, popovers | — |

The kit reads as one product because color resolves to roles, type and spacing
resolve to ramps, voice resolves to a lexicon, and the same tokens drive every
surface. A reviewer can check it line by line: every color has a role and an AA
pair, every value sits on a named scale, and nothing is a one-off.
