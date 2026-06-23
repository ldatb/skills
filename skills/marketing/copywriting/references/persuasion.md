# Persuasion principles and the ethics line

Persuasion changes a decision by giving a real reason to act. Manipulation changes a
decision by exploiting a flaw in how people reason. The line between the two is the spine
of this reference: a tactic is allowed when it would still work after the prospect sees
exactly how it works, and the underlying claim stays true.

This page holds the psychology under the copy. The frameworks in
[frameworks.md](frameworks.md) decide the running order of a page; the principles here
decide *why each beat moves the reader*, and the ethics tests decide *which moves are
off-limits*. Reach for this page when choosing a tactic — scarcity, urgency, social proof,
a trial — and when judging whether that tactic is honest or manipulative. It covers
Cialdini's seven principles, the
conversion-relevant cognitive biases, the ethics line with named dark patterns, the
failure modes, and a worked example on a pricing page.

## Cialdini's seven principles

Robert Cialdini catalogued seven levers of influence across *Influence* and *Pre-Suasion*.
Each lever below carries one honest marketing application and the truth condition that
keeps the lever ethical.

### 1. Reciprocity

People feel obligated to return a favor. A first gift, given freely, raises the odds of a
later yes.

- **Marketing application:** a genuinely useful free resource — a template, an audit, a
  teardown — given before any ask. The gift carries standalone value whether the prospect
  buys or not.
- **Truth condition:** the free thing solves a real problem on its own. A "free" gift that
  is a crippled demo, or that demands payment to unlock the part that matters, is bait.

### 2. Commitment and consistency

People act in line with prior commitments, especially public or written ones. A small
first step makes the next step feel consistent.

- **Marketing application:** a low-friction first action — a short quiz, a one-field signup,
  a starter plan — that fits the prospect's stated goal and leads naturally to the larger
  offer.
- **Truth condition:** the small step serves the prospect, not only the funnel. A first
  step that traps the prospect into a purchase they did not intend weaponizes consistency.

### 3. Social proof

People look to others' behavior to decide their own, hardest under uncertainty. Numbers,
reviews, and peer adoption lower perceived risk.

- **Marketing application:** real customer counts, verifiable testimonials with attribution,
  and named logos the customer agreed to share. Specific proof ("4,200 founders", a named
  case study) beats vague proof ("thousands love us"). The proof hierarchy is detailed in
  [frameworks.md](frameworks.md).
- **Truth condition:** every number and quote is real and current. Fabricated reviews,
  bought followers, and stock-photo "customers" are fraud, not proof.

### 4. Authority

People defer to credible experts and legitimate signals of expertise. Credentials,
track record, and earned media transfer trust.

- **Marketing application:** the founder's actual track record, real certifications, and
  press the product genuinely earned, stated plainly.
- **Truth condition:** the authority is earned and relevant. Borrowed or implied authority —
  a fake "as seen in" strip, an irrelevant degree dressed as proof — misleads.

### 5. Liking

People say yes to those they like — through similarity, warmth, shared values, and genuine
praise. Rapport lowers resistance.

- **Marketing application:** a brand voice that reflects who the founder actually is, shared
  values stated honestly, and copy that talks to the prospect as a peer.
- **Truth condition:** the persona is authentic. A manufactured relatability that hides the
  commercial relationship is a costume, and the prospect feels the seams later.

### 6. Scarcity

People value what is limited or fading. A real deadline or cap raises urgency and the
perceived worth of the offer.

- **Marketing application:** a genuine limit — a cohort that truly caps at 30 seats, a launch
  price that truly ends Friday, inventory that is truly finite — stated with the real reason
  for the limit.
- **Truth condition:** the scarcity is real and the timer means it. A countdown that resets
  on refresh, or "only 2 left" on infinite digital stock, is the single most common dark
  pattern in this list.

### 7. Unity

People act for those who share an identity with them — the "we" of family, tribe, or
community, a step beyond mere liking. Shared identity, not just similarity, drives action.

- **Marketing application:** a real community the prospect belongs to or joins — a founder
  cohort, a category movement, a values-based group — where membership is genuine and
  reciprocal.
- **Truth condition:** the shared identity is real and the prospect is treated as an insider
  in fact, not only in copy. Fake belonging ("join the family") with no community behind it
  rings hollow.

## Cognitive biases relevant to conversion

Biases are systematic deviations in judgment. Used honestly, framing a true offer to match
how people actually decide is fair. Used to engineer a choice the prospect would reject if
they saw clearly, framing becomes manipulation.

### Anchoring

The first number seen sets the reference point against which later numbers are judged. A
high anchor makes a later price feel small.

- **Honest use:** lead with the real full value or list price, then the actual offer price.
- **Line:** the anchor is a real reference (a true list price, a genuine competitor cost),
  not a fictional "was" price that never sold.

### Loss aversion

A loss hurts roughly twice as much as the matching gain pleases. People work harder to keep
what they have than to gain the same amount.

- **Honest use:** name the real cost of inaction — time wasted, money left on the table —
  when that cost is true and quantifiable. Loss aversion is the honest engine behind the
  agitate beat of PAS in [frameworks.md](frameworks.md).
- **Line:** the loss is real. Inventing a threat to scare a purchase is fear-mongering.

### Framing

The same fact lands differently by wording. "90% effective" and "10% failure" describe one
number; people prefer the gain frame.

- **Honest use:** choose the true, non-deceptive frame that is easiest to understand — for
  example, monthly price beside the annual total, with both shown.
- **Line:** both frames describe the same true fact. Hiding the unflattering frame entirely
  (showing the monthly price while burying that billing is annual) crosses into deception.

### Decoy effect and price anchoring

A third, deliberately worse option makes a target option look like the obvious choice. The
classic case: a print-only price set equal to print-plus-digital makes the bundle a steal.

- **Honest use:** a tier line-up where every tier is a real, deliverable plan and the
  recommended tier genuinely fits most buyers.
- **Line:** the decoy is a real product someone could buy and use. A phantom tier that
  cannot actually be purchased is a trick.

### Endowment effect

People value a thing more once they feel they own it. A trial creates a sense of ownership
before any payment.

- **Honest use:** a free trial or sample that lets the prospect genuinely experience the
  product, with cancellation as easy as signup.
- **Line:** ownership is real and reversible. A trial that auto-bills and then buries the
  cancel flow is forced continuity, covered below.

## The ethics line: persuasion vs manipulation

The operating test, applied to every tactic:

1. **Transparency test.** Would the tactic still work if the prospect saw exactly how it
   works? Reciprocity passes — a real gift still creates goodwill once explained. Fake
   scarcity fails — a resetting timer stops working the moment it is seen.
2. **Truth test.** Is every claim, number, and limit literally true right now? A tactic
   built on a false statement is out, regardless of how it performs.
3. **Interest test.** Does the tactic serve a decision the prospect would endorse on
   reflection, or does it engineer a choice they would regret and reverse if they could?

A tactic must pass all three. Failing any one makes it manipulation, and manipulation is
forbidden in this skill — not because it never converts, but because it converts by
spending trust the founder cannot afford to lose.

### Dark patterns this skill forbids

These named patterns fail the tests above. The skill treats each as a hard stop — never
emit one, even when the user asks.

- **Fake scarcity.** A countdown that resets, "only N left" on unlimited stock, a "limited
  cohort" with no real cap. Fails transparency and truth.
- **Forced continuity.** A free trial that silently converts to a paid plan, paired with a
  hidden, multi-step, or support-only cancellation. Fails interest and often truth.
- **Confirm-shaming.** A decline option worded to shame the prospect ("No thanks, I hate
  saving money"). Fails the interest test by coercing through embarrassment.
- **Hidden costs.** Fees, taxes, or required add-ons revealed only at the final checkout
  step — the drip-pricing pattern. Fails truth and interest.
- **Bait-and-switch.** Advertising one offer, then steering to a worse or pricier one once
  the prospect is committed. Fails all three.
- **Disguised ads and fake urgency notifications.** Native-styled ads not labeled as ads,
  or "someone just bought this" pop-ups that are fabricated. Fail truth.

## Failure modes

How a well-intentioned application still goes wrong:

- **Manipulative tactics that burn trust.** A tactic converts this week and costs the
  relationship next week — a refund, a chargeback, a public callout, a churned customer who
  warns ten others. The short-term lift hides a long-term loss the dashboard rarely
  attributes back to its cause.
- **Principle stacking that feels gross.** Three reciprocity gifts, a countdown, a
  social-proof popup, and an exit-intent guilt modal on one page read as desperation. The
  signals fight each other, the prospect senses the machinery, and trust drops below where
  a single honest principle would have left it. One well-chosen principle beats five
  stacked ones.
- **True but irrelevant proof.** Authority or social proof that is real yet unrelated to the
  prospect's actual concern adds clutter and dilutes the genuine signal.
- **Optimizing the metric, not the decision.** A page tuned only for click-through can win
  the click and lose the customer when the post-click reality fails the promise. The right
  measure runs past the conversion to retention and refund rate.
- **Frame that technically passes but reliably misleads.** A wording that is literally true
  yet predictably leaves most readers with a false belief. Literal truth is necessary, not
  sufficient — the test is the belief the frame creates.

## Worked example: an honest pricing page

A founder sells a SaaS product with Starter, Pro, and Team plans. The desired action is a
Pro signup from a qualified small-team buyer. Three principles apply honestly.

**Principle 1 — price anchoring with a real tier line-up.** The page shows all three plans
side by side. Team is priced highest and listed first, anchoring the buyer high; Pro sits
in the middle, marked "Most popular" because it genuinely is the most-purchased plan. Every
tier is a real, deliverable product. No phantom decoy exists.

> Why it passes: the anchor (Team's price) is a true list price, the "Most popular" badge
> reflects real purchase data, and the buyer who inspects every tier finds each one buyable.
> Transparency, truth, and interest all hold.

**Principle 2 — social proof, specific and verifiable.** Under Pro sits one line: "Used by
1,180 small teams" beside two named testimonials with company and role, each linking to a
full case study. The number is pulled from the live customer count.

> Why it passes: the count is real and current, the testimonials are attributed and
> checkable, and the proof speaks to the exact buyer (small teams). Showing the source-of-
> truth count would not weaken it — transparency holds.

**Principle 3 — framing the price honestly.** Pro shows the monthly figure in large type
with "billed annually at $X" directly beneath in equal-weight text, plus a visible monthly
billing toggle. The gain frame (low monthly number) leads, but the full annual commitment is
stated in the same breath, not buried.

> Why it passes: both frames describe one true price, the annual total is not hidden, and the
> toggle lets the buyer choose. The unflattering frame is present, so the framing informs
> rather than deceives.

**What the page refuses.** No countdown timer (there is no real deadline). No "3 people are
viewing this" widget (fabricated). No pre-checked annual upsell (forced). The decline path
on the email-capture modal reads "No thanks" — plain, not shaming. Checkout shows the final
total, tax included, before the card field — no drip pricing.

**How the founder measures it.** The primary metric is qualified Pro signups, not raw
clicks. The page is judged across the full funnel: signup rate, then 90-day retention and
refund rate. A variant that lifts signups but raises refunds has not won — it has moved the
cost downstream. An A/B test changes one principle at a time so the founder learns which
honest lever actually moved the decision.
