# Retention playbook

Churn is the rate at which paying customers stop paying. Retention is the inverse,
and retention compounds: a product that keeps 95% of revenue each month is a
different business from one that keeps 80%, even at identical acquisition. The
leverage in churn work is **leading**, not lagging — a cancellation is the lagging
confirmation of a decision the customer made weeks earlier. This playbook names the
signals that precede the decision, the segments that carry different risk, the
intervention matched to each driver, and the metrics that prove the work moved the
number.

A founder's instinct is to fight churn with a discount. A discount treats price as
the driver when price is rarely the driver. Diagnose first; the intervention is
downstream of the cause.

## 1. Leading churn signals

A leading signal is an observable change that predicts cancellation before the
customer asks to leave. The four below carry the most predictive weight for a SaaS
product. Track each as a trend against the account's own baseline, not against a
global average — a power user dropping to half their normal usage is at higher risk
than a light user at their steady normal.

- **Usage decay.** Logins, core-action counts, or active seats fall against the
  account's trailing baseline. Usage is the strongest single predictor, because a
  product that stops being used stops being valued. A 30%+ drop in weekly active
  use over two consecutive weeks is a standard at-risk threshold.
- **Failed payments.** A card declines, expires, or hits a limit. This signal is
  involuntary churn in progress, and the customer often does not know the charge
  failed. The fix is operational (dunning), not persuasive.
- **Support sentiment.** Ticket volume rises, tone sours, or a customer files a bug
  on a workflow they depend on. A single angry ticket about a core workflow predicts
  churn better than ten neutral tickets about edge cases.
- **Unmet activation.** A new account never reaches the action that delivers first
  value (the "aha" moment). An account that never activates was never retained — it
  was a trial that had not yet expired.

Red flag: a dashboard that shows only MRR and cancellation count. Both are lagging.
A retention program without leading signals is a program that learns of every loss
too late to prevent it.

## 2. The activation-to-retention link

Most "churn" in an early-stage product is failed activation wearing a later date.
A customer who never reaches first value has no reason to stay, so the single
highest-leverage retention investment is usually onboarding, not win-back.

- Define the **activation event** as the specific first action correlated with
  long-term retention (the team invited a second member; the first report was
  exported; the integration fired once). Name one event, measured, not a vague
  "got value."
- Measure **time-to-value** from signup to that event. A shorter time-to-value
  raises the share of accounts that survive their first cycle.
- Treat the activation rate as a retention metric. Lifting activation from 40% to
  60% moves the entire downstream cohort curve up, with no change to any save play.

Red flag: pouring spend into win-back offers while activation sits under 50%. The
bucket leaks at the top; patching the bottom wastes the offer budget.

## 3. Segmentation

A single average churn rate hides the accounts that need action. Segment the base
by health so each intervention reaches the accounts it fits. Three segments cover
most products; score every account into exactly one.

- **At-risk.** One or more leading signals fired: usage decay, a failed payment, a
  sour support thread, or stalled activation. These accounts are the target of
  active intervention.
- **Healthy.** Steady usage at or above their baseline, current on payment, neutral
  or positive support history. The play here is to protect the steady state and
  nudge toward deeper adoption, not to interrupt with a save offer.
- **Power users.** Usage and breadth well above the cohort, multiple active seats or
  workflows. These accounts are expansion and advocacy candidates; the retention
  risk is concentrated key-person dependence and under-served growth, not apathy.

A health score combines the signals into one number per account: usage trend,
payment status, support sentiment, and activation depth, each weighted, summed, and
bucketed. The score is the routing key for the playbooks below.

Red flag: one retention email to the whole list. A save offer sent to a healthy
power user teaches them the product is overpriced and trains them to wait for a
discount.

## 4. Intervention playbooks by segment

Match the play to the driver, not to the calendar. Each play below names its
trigger, its message, and the metric that closes it.

### Onboarding nudge — driver: stalled activation

- Trigger: a new account has not reached the activation event within the expected
  time-to-value window.
- Play: a guided, specific next step toward first value — a setup checklist, a
  templated starter, a short call for a high-value account. Remove the one step
  where accounts stall, rather than restating the whole tour.
- Closes when: the account fires the activation event, or the play is marked failed
  and the account is re-scored.

### Value reminder — driver: usage decay in a healthy account

- Trigger: usage falls against baseline, with no payment or support signal.
- Play: surface realized value (a usage recap, an outcome the customer achieved, an
  unused capability tied to their goal). Re-anchor the product to the job the
  customer hired it for. Carry no discount.
- Closes when: usage recovers toward baseline, or the account escalates to the save
  play after a set window.

### Save offer — driver: a stated intent to cancel

- Trigger: the customer reaches the cancel flow, requests a downgrade, or explicitly
  signals leaving.
- Play: lead with diagnosis — a one-question "what changed?" — then match the
  response. A pause beats a cancel; a plan-fit change beats a discount; a missing
  feature earns an honest roadmap answer, not a price cut. Price concessions are the
  last lever, reserved for confirmed price-driven churn, time-boxed and tracked.
- Closes when: the customer stays on a defined plan, accepts a pause, or churns with
  a recorded reason that feeds the loop.

### Win-back — driver: an already-churned account

- Trigger: the account has cancelled and a cooling-off period has passed.
- Play: target only churned accounts whose exit reason has since been addressed (the
  missing feature shipped; the bug closed; a new plan fits). A win-back to an account
  whose reason still stands is spam.
- Closes when: the account reactivates, or is suppressed from further win-back after
  a capped number of attempts.

## 5. Voluntary vs involuntary churn

Voluntary churn is a decision: the customer chose to leave. Involuntary churn is a
failure: a payment broke and the account lapsed without a decision. The two have
different owners and different fixes, and conflating them buries a recoverable loss
inside a behavioral one.

- **Voluntary** is addressed by the diagnose-and-intervene loop above: signals,
  segmentation, and a play matched to the driver.
- **Involuntary** is addressed by **dunning** — the automated recovery of failed
  payments. A dunning sequence retries the charge on a schedule, emails the customer
  to update the card, and applies a grace period before the account is suspended.
  Card pre-expiry reminders and account-updater services prevent the failure before
  it happens.

Involuntary churn is commonly 20-40% of total churn and is the cheapest to recover,
because the customer already wants the product — the only obstacle is a broken
charge. A retention program that ignores dunning leaves recoverable revenue on the
floor.

Red flag: counting an expired-card lapse as a customer who "left." That account did
not decide to leave; the billing system decided for it.

## 6. The metrics

Track retention with cohort-anchored, revenue-aware metrics. A single blended churn
percentage averages away the signal.

- **Gross revenue retention (GRR).** Revenue retained from a cohort over a period,
  excluding expansion, capped at 100%. GRR isolates pure leakage — churn plus
  contraction — and is the truest measure of how well the product holds value.
- **Net revenue retention (NRR).** Revenue retained including expansion from the same
  cohort. NRR above 100% means the surviving base grows faster than it leaks, the
  signature of a durable SaaS. NRR can hide churn behind a few expanding whales, so
  read it beside GRR, never alone.
- **Logo churn.** The count of accounts lost over a period, regardless of size. Logo
  churn and revenue churn diverge when small accounts leave and large ones expand;
  watch both, because a product losing many small logos has a product-market-fit
  signal even while revenue looks fine.
- **Cohort retention curves.** Each signup cohort plotted as the share still active
  over time. A healthy curve flattens to a stable plateau; a curve that decays to
  zero has no retained core. The flattening point, and its height, is the single most
  honest picture of retention.

Read these together. NRR alone flatters; logo churn alone ignores value; a blended
average alone hides the cohort that is bleeding.

## 7. Failure modes

- **Treating all churn the same.** One average, one email, one offer. A failed
  payment, a stalled trial, and a deliberate cancel have nothing in common but the
  outcome. Undiagnosed churn gets the wrong fix every time.
- **Discount-only saves.** Reflexively offering money at the cancel flow. A discount
  trains customers to threaten cancellation for a price cut, erodes margin, and
  leaves the real driver — a missing feature, a failed onboarding — untouched. The
  account churns later anyway, now at a lower price.
- **No leading signals.** Measuring only MRR and cancellations. Both confirm losses
  after the window to prevent them has closed. A program with no leading signal is a
  post-mortem service, not a retention program.
- **Saving accounts that should churn.** Spending retention effort on a poor-fit
  customer who will churn regardless and complain loudly meanwhile. Some churn is
  healthy; a wrong-fit account freed is capacity returned.
- **Vanity NRR.** Reporting NRR above 100% while a long tail of small logos bleeds
  out. Expansion from a few accounts masks a product-market-fit problem in the base.

## 8. Red flags

- The only retention metric on the dashboard is MRR or total cancellations.
- The cancel flow's first move is a discount, before any diagnostic question.
- Failed payments are counted as voluntary churn, with no dunning sequence.
- One retention message addresses the entire base regardless of health.
- Activation rate is unknown or under 50%, while win-back spend rises.
- Reported NRR exceeds 100% while logo churn climbs and no one reads the cohort curve.
- "Why did they leave?" has no recorded, structured answer for past cancellations.

## 9. Worked example — an at-risk intervention

**Account.** A 12-seat team on a $600/month plan, eight months tenured, previously
healthy.

**Signal.** The health score drops. Weekly active seats fell from 10 to 4 over two
weeks (a 60% usage decay), no payment failure, one support ticket last week reading
"the new export layout broke our workflow." Segmentation routes the account to
**at-risk**, driver **usage decay tied to a product change**, not price.

**Diagnosis.** The usage drop tracks the support ticket: a release changed the export
the team depended on daily. This is a product-driven decay, so the wrong play is a
save offer (no intent to cancel yet) and the wrong play is a discount (price is not
the driver). The right play is a **value reminder fused with issue resolution**.

**Intervention.** A named human (founder or CS) replies to the ticket within a day,
confirms the export regression, gives a concrete workaround now and a fix date.
A short follow-up re-anchors value with a usage recap from the account's healthy
months. No discount is offered, because the driver is product, not price.

**Measurement.** The closing metric is usage recovery, not the reply itself. Track
weekly active seats back toward the 10-seat baseline over the next two cycles. If
seats recover, the play closed successfully; if they keep falling, the account
escalates to the save play and the export regression is flagged as a churn driver
for other accounts on the same release.

**Loop.** The export regression is recorded as a churn signal and checked against the
broader at-risk segment, because one account hitting a release-driven decay predicts
others on the same release will follow. The diagnosis feeds back into the leading
signals so the next occurrence routes faster.
