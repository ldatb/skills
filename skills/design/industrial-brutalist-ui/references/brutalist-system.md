# The industrial / neo-brutalist UI system

Neo-brutalism borrows from the concrete brutalism of 1950s architecture: structure
left exposed, material shown raw, ornament refused. Applied to a screen, the style
exposes the grid, leans on system and monospace type, swaps soft shadows and gradients
for hard edges and flat fills, and treats friction as a stylistic signal rather than a
flaw. The aesthetic reads as deliberate, confident, and a little confrontational.

Done badly, the same moves read as a broken stylesheet. The line between "distinctive"
and "unusable" is contrast, legibility, and keyboard support — the style permits a raw
look, never an inaccessible one. This reference draws that line and shows where to stand.

## Principles

Eight commitments separate intentional brutalism from a half-finished theme:

1. **Raw structure exposed.** Show the skeleton: visible containers, hard dividing
   lines, labelled regions. The layout admits what it is instead of smoothing itself away.
2. **High contrast.** Near-black on near-white (or the inverse) is the default. Mid-grey
   text on a grey panel is the cardinal sin of the style.
3. **Heavy, monospaced, or grotesque type.** Bold weights, tight tracking, and a
   monospace or industrial grotesk face carry the voice. Type is a structural element,
   not a polite caption.
4. **Visible grid.** A column grid the eye can read — wide gutters, hard alignment,
   blocks that snap to lines — over an invisibly balanced composition.
5. **Hard edges over soft rounding.** Square corners or a small, fixed radius. Pillowy
   `border-radius` and blurred shadows belong to a different aesthetic.
6. **Flat over skeuomorphic.** Solid fills, no gradients, no glassmorphism, no embossing.
   A surface is a coloured rectangle with a border, not a faux-physical object.
7. **Function-forward.** Controls announce themselves as controls. A button looks
   pressable because it is a heavy bordered block, not because it mimics a real object.
8. **Deliberate "ugly."** The style courts the unfashionable on purpose — clashing
   accents, oversized labels, exposed seams. Deliberate is the operative word; the
   roughness is authored, never an accident left in.

## Building blocks

The vocabulary that renders the principles in CSS:

- **Borders.** Thick, solid, single-colour strokes — `2px` to `4px`, occasionally
  heavier. The border is the primary device for separating regions, and it carries the
  hierarchy a soft shadow would carry elsewhere.
- **Blocks.** Rectangular, hard-aligned panels in solid fills. Whitespace is generous
  and squared-off rather than softly cushioned.
- **Monospace and grotesque type.** A monospace face (or a heavy grotesk) for labels,
  data, and UI chrome. Tabular figures and a fixed character cell reinforce the
  machined, structural feel.
- **A limited, stark palette.** One paper, one ink, and one or two loud accents — hazard
  yellow, electric blue, hot red. The restraint is what keeps the loudness legible.
- **Oversized type.** Headings several steps larger than a conventional scale, set in
  bold or black weights. Scale itself becomes the ornament.
- **Offset hard shadows.** A solid, un-blurred drop shadow — `box-shadow: 6px 6px 0
  var(--ink)` — that reads as a second hard-edged rectangle, not a soft glow. The signature
  move of the style.

## When the aesthetic fits

The style earns its place where personality outranks reassurance:

- **Developer tools and technical products.** A monospace, grid-exposed look matches the
  mental model of the audience and signals that the product respects raw information.
- **Indie products, portfolios, and side projects.** A solo or small team uses brutalism
  to stand apart from templated SaaS sameness on a near-zero design budget.
- **Statement brands and editorial.** A fashion drop, a music label, a manifesto site, or
  a conference page uses the confrontational look as the message itself.

What these share: an audience that rewards a strong point of view, and stakes low enough
that a moment of visual friction costs a raised eyebrow, never a lost user.

## When the aesthetic does not fit

The same friction that reads as confidence elsewhere reads as risk here:

- **Trust-sensitive flows.** Banking, healthcare, insurance, and government services trade
  on calm and credibility. A look that courts "ugly" undermines the reassurance these
  flows exist to provide.
- **Broad-consumer products at scale.** A mainstream audience spanning every age and
  ability skews conservative. An unconventional look raises the bricks-and-mortar
  question — "is this real?" — at the worst moment.
- **Accessibility-critical, high-stakes paths.** A checkout, a medication dose entry, a
  legal consent step has no tolerance for a decorative choice that costs a single user the
  task. Clarity outranks character whenever the cost of a mistake is high.

The decision rule: when a single confused user is an expensive failure, the raw look is a
liability, and a calmer system wins.

## Keeping it accessible

The raw look is a visual style, never a licence to drop accessibility. The style actually
starts from an advantage — high contrast and large type are baked into its DNA — so the
work is holding that advantage through the interactive states.

- **Contrast.** Hold every text-on-background pair at WCAG AA: 4.5:1 for body text, 3:1
  for large text and for the borders that carry meaning. A loud accent used as a text
  colour gets the same measurement as any other colour.
- **Focus.** A keyboard focus state must be visible and distinct from hover. A thick
  offset outline (a second hard ring in the accent colour) suits the aesthetic and reads
  unmistakably, so the style and the requirement reinforce each other.
- **Hit targets.** Interactive controls clear a 44x44px minimum touch target. Heavy
  padding fits the blocky look and lands the target size at the same time.
- **Beyond colour.** A loud accent cannot be the only signal of state or meaning. Pair it
  with a label, an icon, a border-weight change, or a fill change so a colour-blind user
  loses nothing.
- **Motion and type.** Keep monospace body copy short to protect reading speed, and honour
  `prefers-reduced-motion` on the hard transitions the style favours.

## Failure modes

Three ways the style collapses, each a real bug rather than a matter of taste:

1. **Edgy but illegible.** Type so heavy, tracking so tight, or accents so loud that
   reading slows to a crawl. The style is supposed to read *more* boldly, never *less*
   clearly — illegible defeats the entire point.
2. **Brutalism as an excuse for low effort.** Unstyled HTML relabelled as "raw" and
   shipped. True brutalism is highly composed — deliberate grid, deliberate scale,
   deliberate restraint. A skipped design pass is not a style.
3. **Poor contrast hiding behind aesthetics.** Mid-grey on grey or accent-on-accent
   excused as "the look." Contrast is a measurable floor, and the aesthetic never lowers
   it.

## Red flags

Signals that a brutalist design has crossed from distinctive into broken:

- A text-on-background pair below 4.5:1 (body) or 3:1 (large), justified as "part of the
  style."
- A keyboard focus state that is missing, or identical to the hover state.
- A loud accent doing semantic work — error, success, selected — with no second signal
  besides the colour.
- A touch target under 44x44px crammed by tight blocking.
- Body text set in a heavy monospace at length, where reading speed collapses.
- "Raw" used as the reason a screen received no real design pass.
- A trust-sensitive or high-stakes flow wearing the confrontational look against its own
  goal.
- Hard offset shadows or thick borders stacked so densely the actual content gets lost in
  the chrome.

## Worked example: a card with a button set

Goal: a "Deploy" card in full neo-brutalist dress that still clears AA contrast and full
keyboard support. The example keeps the loud look and removes every red flag above.

### Tokens

```css
:root {
  --paper:  #f4f4ec;  /* warm off-white background      */
  --ink:    #14110f;  /* near-black text and borders    */
  --accent: #1f57ff;  /* electric blue, primary action  */
  --hazard: #ffd400;  /* hazard yellow, attention only  */
  --danger: #d4351c;  /* destructive action             */
  --radius: 0px;      /* hard corners                   */
  --border: 3px solid var(--ink);
  --shadow: 6px 6px 0 var(--ink);  /* solid offset, no blur */
}
```

Contrast check (computed, not guessed):

- `--ink` `#14110f` on `--paper` `#f4f4ec` ≈ **17.4:1** — passes AA and AAA for body.
- White `#ffffff` on `--accent` `#1f57ff` ≈ **5.6:1** — passes AA for the button label.
- `--ink` `#14110f` on `--hazard` `#ffd400` ≈ **13.6:1** — the yellow carries dark text,
  never white.
- White on `--danger` `#d4351c` ≈ **4.7:1** — passes AA for the destructive label.

### Markup

```html
<article class="brut-card" aria-labelledby="deploy-title">
  <span class="brut-tag">PRODUCTION</span>
  <h2 id="deploy-title" class="brut-title">DEPLOY BUILD #4271</h2>
  <p class="brut-body">Commit 9f3ac1 · main · 12 files changed</p>
  <div class="brut-actions">
    <button type="button" class="brut-btn brut-btn--primary">Deploy</button>
    <button type="button" class="brut-btn brut-btn--ghost">Preview</button>
    <button type="button" class="brut-btn brut-btn--danger">Roll back</button>
  </div>
</article>
```

### Styles

```css
.brut-card {
  background: var(--paper);
  color: var(--ink);
  border: var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 24px;
  max-width: 28rem;
  font-family: "JetBrains Mono", ui-monospace, "SFMono-Regular", monospace;
}

.brut-tag {
  display: inline-block;
  background: var(--hazard);
  color: var(--ink);              /* dark on yellow, 13.6:1 */
  border: var(--border);
  padding: 2px 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
}

.brut-title {
  font-size: 2rem;                /* oversized, structural  */
  font-weight: 800;
  line-height: 1.05;
  margin: 16px 0 8px;
}

.brut-body {
  font-size: 0.95rem;
  line-height: 1.5;               /* short line, kept readable */
  margin: 0 0 20px;
}

.brut-actions { display: flex; gap: 12px; flex-wrap: wrap; }

.brut-btn {
  font: inherit;
  font-weight: 700;
  border: var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 12px 20px;             /* clears the 44px target */
  min-height: 44px;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease;
}

.brut-btn--primary { background: var(--accent); color: #fff; }
.brut-btn--ghost   { background: var(--paper);  color: var(--ink); }
.brut-btn--danger  { background: var(--danger); color: #fff; }

/* Press: the block physically sinks into its own shadow */
.brut-btn:active {
  transform: translate(3px, 3px);
  box-shadow: 3px 3px 0 var(--ink);
}

/* Hover stays distinct from focus */
.brut-btn:hover { transform: translate(-1px, -1px); box-shadow: 8px 8px 0 var(--ink); }

/* Keyboard focus: a second hard ring, never identical to hover */
.brut-btn:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 3px;
}
.brut-btn--primary:focus-visible { outline-color: var(--ink); }

@media (prefers-reduced-motion: reduce) {
  .brut-btn { transition: none; }
  .brut-btn:active, .brut-btn:hover { transform: none; }
}
```

### Why this passes

- **Looks brutalist:** hard `0px` corners, `3px` ink borders, solid offset shadows, a
  monospace face, oversized heading, hazard-yellow tag, electric-blue primary — the full
  vocabulary.
- **Stays legible:** every label and body pair measured at AA or above; the yellow and
  blue each carry the text colour that clears the ratio.
- **Stays operable:** `:focus-visible` gives a distinct accent ring separate from hover;
  the destructive action reads as red *and* as a labelled "Roll back," so colour is never
  the sole signal; padding plus `min-height` clear 44px; reduced-motion disables the hard
  transitions.

The card proves the thesis of this skill: the raw look is fully compatible with the
accessibility floor. Brutalism is an aesthetic of exposed structure — never an excuse to
expose the user to a broken experience.
