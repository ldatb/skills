# The overdrive protocol

Overdrive is maximum-effort mode: a deliberate escalation of rigor far above the
default, reserved for tasks where being wrong is expensive. The default pass is tuned
for throughput and good-enough correctness. Overdrive is tuned for surviving scrutiny:
adversarial review, a security audit, a production incident, a customer who will notice
the one case the demo skipped.

The mode is not "try harder" as a vibe. The mode is a fixed set of changes to the
process, engaged on purpose, paid for in time and tokens, and switched off again once
the task no longer justifies the spend. Spending overdrive effort on a throwaway is a
failure of judgment, the gold-plating the [foundation doctrine](../../../meta/foundation/SKILL.md)
treats as waste. Effort without aim is not rigor; aimless effort is merely cost.

## What overdrive changes versus normal work

A normal pass produces one reasonable solution, checks the happy path, trusts the
obvious claims, and ships. Overdrive replaces each of those defaults with a stricter
discipline.

| Dimension | Normal pass | Overdrive pass |
|---|---|---|
| Solution space | First workable approach | Two or three independent approaches, scored, best chosen |
| Claims | Asserted from reasoning | Verified against real output (Genchi Genbutsu) |
| Edge cases | Happy path, obvious guards | Boundary, empty, large, malformed, concurrent — enumerated, then resolved |
| Self-review | A quick reread | Adversarial critique: attack the weakest assumption first |
| Tooling | Run if convenient | Lint, types, tests, and a second tool cross-check the result |
| Assumptions | Left implicit | Surfaced and either verified or recorded as a known limitation |

The six concrete shifts:

1. **Generate multiple independent approaches and pick the best.** One approach hides
   its own blind spots. A second and third, derived independently rather than as
   tweaks of the first, expose the trade-offs the first one buried. Score the
   candidates against the actual stake, then commit to one with a written rationale
   for the rejection of the others.

2. **Verify every claim against real output.** A claim the deliverable depends on gets
   confirmed by running the code, the query, or the command, never by asserting the
   answer the model expects. Observation beats prediction; the gap between "should
   work" and "does work" is where defects live.

3. **Enumerate edge cases exhaustively.** The boundary, empty, large, malformed, and
   concurrent inputs each get listed before any of them gets handled. An enumerated
   list can be checked for completeness; a vague intention to "cover edge cases"
   cannot.

4. **Self-critique adversarially.** The author argues against the work as a hostile
   reviewer would, naming the weakest assumption and the likeliest failure, then
   answers each objection or accepts it as a documented limitation. Praise is not
   review; an unanswered objection is a finding, not a footnote.

5. **Cross-check with tools and tests.** The result faces a second, independent
   verifier: a linter, a type checker, a test suite, a diff against a reference
   implementation. A defect that one method misses, a second method tends to catch.

6. **Leave nothing assumed.** A load-bearing assumption gets surfaced and either
   verified or written down as a known unknown with its risk stated. A silent
   assumption is a latent bug with a deadline.

## When overdrive is warranted

Engage the mode when the cost of being wrong dwarfs the cost of the extra effort. The
qualifying conditions:

- **High stakes.** A wrong answer damages users, revenue, reputation, or safety.
- **Irreversibility.** The action is hard or impossible to undo: a destructive
  migration, a public release, a payment, a deletion, a signed contract.
- **Security or financial sensitivity.** The change touches auth, secrets, money
  movement, access control, or personal data, where one missed case is an exploit.
- **A flagship deliverable.** The work is the headline artifact, judged on its own,
  carrying outsized visibility or precedent.

Any one condition can justify overdrive. Two or more make it close to mandatory.

## When overdrive is wasteful

Skip the mode, and take the default pass, when the stakes do not clear the bar.
Overdrive on the wrong task is a failure of the same kind as a sloppy pass on a
critical one — both spend effort in the wrong place.

- **Throwaway work.** A one-off script, a scratch query, a spike deleted within the
  hour earns no second approach.
- **Exploratory work.** During discovery the goal is learning fast, and premature
  rigor freezes a direction the work has not yet earned.
- **Trivial work.** A typo fix, a config bump, a rename does not merit three
  candidate designs and an adversarial review.

Gold-plating is a failure mode, not a virtue. The Kanso principle holds even here: the
shortest path that meets the real stake wins, and rigor beyond the stake is waste
dressed as diligence.

## The cost, and how to decide

Overdrive is not free. The bill is roughly three-to-ten times the time and tokens of a
default pass: multiple approaches drafted, output captured and read, edge cases
enumerated and resolved, an adversarial review round, tool cross-checks. On a task that
warrants it, that spend is cheap against the cost of a production incident or a public
retraction. On a task that does not, the same spend is pure waste.

Decide with a single explicit comparison, written down before engaging:

1. State the **stake** in one sentence: what breaks, and how badly, if the work is
   wrong.
2. Estimate the **cost** of overdrive in extra passes against the cost of the default
   pass plus the expected cost of a defect slipping through.
3. Engage overdrive only when the stake times the defect probability exceeds the extra
   effort. Otherwise take the default pass and record that choice.

The decision is itself a checkable artifact, not a feeling. A reader can audit the two
sentences and agree or disagree.

## Relationship to verification and polish

Overdrive does not replace verification-before-completion; overdrive raises its
ceiling. The verification discipline says: prove the work does what it claims before
calling it done. Overdrive applies that proof to a wider surface — multiple approaches,
exhaustive edge cases, adversarial objections — and demands the proof rest on observed
output rather than reasoning.

Polish is the adjacent refinement pass: the last increment of quality on work that is
already correct. The boundary is clean. Polish improves a correct result; overdrive
establishes that the result is correct and complete under pressure in the first place.
A flagship deliverable often wants both, in order: overdrive to get it right, then
polish to make it inevitable. Polishing an unverified result is rearranging a facade
over an unchecked foundation.

## Failure modes

- **Overdrive on the wrong task.** The most common failure: maximum effort poured into
  a throwaway, an exploratory spike, or a triviality. The fix is the decision gate —
  justify the spend before engaging, and abort to the default pass when the stake does
  not clear the bar.
- **Perfectionism paralysis.** Endless refinement with no shipping criterion, each
  pass finding a smaller flaw. The fix is checkable completion: every step ends on an
  observable condition, and the work ships when the conditions are met rather than when
  the author feels satisfied.
- **Effort without direction.** Hours spent on the easy, visible parts while the actual
  risk goes untouched — three beautiful approaches to a problem that was never the
  stake. The fix is to anchor each step to the stated stake, dropping any work whose
  contribution to the stated risk is nil.
- **Theater over substance.** The ritual performed without the rigor: candidates named
  but not genuinely independent, claims "verified" without running anything, a critique
  that lists no real objection. The fix is the observable criterion behind each step,
  which a reviewer can confirm was actually met.

## Red flags

A pull toward any of these signals overdrive has gone wrong:

- The deliverable is a scratch file, a spike, or a triviality, and the effort is
  climbing anyway.
- Three "independent" approaches differ only in naming or formatting.
- A claim reads "this works" with no captured output behind it.
- The edge-case list was skipped because the happy path "obviously" covers them.
- The self-critique found nothing wrong.
- The effort concentrated on the parts that were already safe.
- No shipping criterion exists, and each pass invents a new flaw to fix.
- The stake was never written down, so the spend cannot be justified.

## Worked example: normal versus overdrive

**Task.** Write a function that parses a user-supplied date range string such as
`2026-01-01..2026-03-31` into a start and end date.

### The normal pass

A normal pass is appropriate when this parser feeds an internal dashboard filter where
a bad input merely shows no rows.

1. Split the string on `..`, parse each half with the standard library, return the
   pair.
2. Test the one happy-path example from the ticket. The bar is green.
3. Ship.

The result handles the demo input. The reversed range, the missing half, the malformed
date, the open-ended range, and the timezone of the boundaries are all unconsidered.
For an internal filter, that is an acceptable trade: the stake is low, and the default
pass matches it.

### The overdrive pass

Overdrive is appropriate when the same parser drives a billing export, where a wrong
range over-charges or under-charges real customers — high stakes, financial
sensitivity, hard to undo once invoices send.

1. **Justify the spend.** Stake: a misparsed range bills the wrong period across the
   whole customer set on the export. Payoff: the extra effort is trivial against a billing
   incident. Overdrive is warranted.
2. **Generate approaches.** (a) Hand-rolled split and parse. (b) A parser-combinator
   over a small grammar. (c) A vetted date-range library. Score against the stake:
   the library carries the fewest hand-written edge cases for a billing path, so it
   wins; the rationale for rejecting the hand-rolled version is recorded.
3. **Verify against real output.** Run the chosen parser on the ticket example and read
   the returned pair, rather than asserting it. The output confirms the boundaries.
4. **Enumerate edge cases.** Reversed range; one half missing; a non-date half; an
   open-ended range (`2026-01-01..`); a single instant; an invalid calendar date
   (`2026-02-30`); the inclusive-or-exclusive question for the end boundary; the
   timezone the dates resolve in. Each listed case gets a defined behavior, with a
   rejecting error for the malformed ones.
5. **Self-critique adversarially.** Weakest assumption: the end date is inclusive — a
   wrong guess shifts a full day of billing. The objection is answered by pinning the
   contract in a test and documenting it at the call site.
6. **Cross-check with tools and tests.** The lint, type, and test gates run green; a
   property test feeds random valid and invalid strings and asserts that no malformed
   input ever yields a silently wrong range.
7. **Decide done.** Steps 1 through 6 each reported their criterion, and the effort
   stayed on the billing risk rather than drifting into parser elegance. Done.

The two passes solve the same surface problem. The normal pass is correct for a filter
and reckless for a billing export; the overdrive pass is correct for a billing export
and wasteful for a filter. The skill is not "always do the second one" — the skill is
matching the rigor to the stake, and writing down the match so a reviewer can check it.

## Checkable criteria

An overdrive pass is complete when each holds:

- The stake and the cost-benefit decision are written in two sentences, and the payoff
  exceeds the cost.
- At least two genuinely independent approaches were produced and scored, with a
  recorded rationale for the chosen one.
- No load-bearing claim rests on assumption; each cites the observed output that
  confirms it.
- The edge-case list is enumerated and exhausted, with a resolution or a recorded skip
  reason against each listed case.
- The strongest adversarial objection has a written answer or an accepted, documented
  limitation.
- The lint, type, and test gates exit zero, with any residual failure recorded as a
  known finding.
- The effort stayed aimed at the stated stake, confirmed in one closing sentence.
