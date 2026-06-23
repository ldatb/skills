# Growth reference: measuring growth — funnel and revenue metrics

Measuring growth makes a founder's revenue **predictable**: one funnel that every
function reads the same way, metrics computed from one source of truth, and handoffs
that lose no deal between marketing, sales, and success. The aim is not more
dashboards — the aim is a number a founder can trust enough to forecast against and act
on. The funnel sits in the middle of the growth loop: a [prioritized
idea](idea-generation.md) is a bet, and the funnel is what proves whether the bet paid.

A funnel a founder cannot reason about is worse than no funnel: a false funnel
manufactures false confidence. The standard below trades flexibility for that trust.
Every stage has one entry condition, every metric has one formula, and every handoff
has one owner.

## The funnel stages

A stage is a state a prospect occupies, defined by an **entry condition** that is
observable in the system of record — not a feeling, not a rep's optimism. The
condition is binary: the record either meets it or does not.

| Stage | Entry condition (when the record enters) | Owner |
|-------|-------------------------------------------|-------|
| **Lead** | A contact exists with a name and a reachable channel (email or phone). | Marketing |
| **MQL** (marketing-qualified lead) | The lead crossed a fit-and-intent threshold: matches the ICP and took a scored action (demo request, pricing view, high lead score). | Marketing |
| **SQL** (sales-qualified lead) | Sales accepted the MQL after a qualification call confirming need, authority, and timeline. | Sales |
| **Opportunity** | A deal record exists with an amount and a target close date; the prospect agreed to evaluate. | Sales |
| **Closed-won** | The contract is signed and revenue is booked. | Sales |
| **Closed-lost** | The deal ended without a signature; a loss reason is recorded. | Sales |
| **Expansion** | An existing customer added seats, upgraded a tier, or bought a second product. | Success |
| **Churn** | An existing customer cancelled or failed to renew; a churn reason is recorded. | Success |

Two rules keep stages honest:

- **Forward-only by default.** A record advances one stage at a time. A skipped stage
  means the entry condition for the skipped stage was never checked — the data lies
  about where deals actually are.
- **One definition, repo-wide.** "MQL" means the same thing on the marketing
  dashboard, the sales pipeline, and the board deck. A stage with two readings is two
  stages wearing one name.

## The core metrics

Every metric below is a ratio or a duration computed from stage timestamps and booked
amounts. No metric depends on judgment at read time — the judgment is spent once, when
the stage definitions are set.

### Acquisition economics

- **CAC** (customer acquisition cost) = total sales-and-marketing spend in a period ÷
  new customers won in that period. Count fully-loaded spend: ad spend, salaries,
  tooling, commissions.
- **LTV** (lifetime value) = average revenue per customer per period × gross margin ×
  average customer lifetime. Lifetime in periods = 1 ÷ churn rate. Use gross margin,
  not raw revenue — a dollar of revenue that costs 70 cents to serve is worth 30 cents.
- **LTV:CAC ratio** = LTV ÷ CAC. The headline efficiency number. A healthy SaaS target
  sits near 3:1 — below 1:1 the business loses money on each customer; far above 5:1
  usually signals underinvestment in growth, not virtue.
- **Payback period** = CAC ÷ (monthly revenue per customer × gross margin). The count
  of months until a customer repays their acquisition cost. Under 12 months is strong
  for early-stage SaaS; over 18 months strains cash.

### Flow and conversion

- **Stage conversion rate** = records entering stage N+1 ÷ records that entered stage N,
  over the same cohort. One rate per adjacent pair (lead→MQL, MQL→SQL, SQL→opp,
  opp→won).
- **Win rate** = closed-won ÷ (closed-won + closed-lost), measured on deals that
  reached a terminal state. Open opportunities are excluded — counting them deflates
  the rate and hides the true close probability.
- **Pipeline coverage** = open pipeline value ÷ the revenue target for the period. A
  coverage of 3× to 4× is the usual floor: at a 25%–33% opp→won rate, 3×–4× pipeline is
  what closes the number.
- **Sales-cycle length** = median days from opportunity created to closed-won. Use the
  median, not the mean — one nine-month enterprise deal drags the mean and lies about
  the typical deal.

### Retention

- **NRR** (net revenue retention) = (starting recurring revenue of a cohort + expansion
  − contraction − churn) ÷ starting recurring revenue, over a year. Above 100% means
  the existing base grows without a single new logo; under 100% means the business
  leaks revenue faster than it expands and growth must outrun a draining bucket.
- **Gross retention** = (starting recurring revenue − contraction − churn) ÷ starting
  recurring revenue. Caps at 100%; isolates leakage from expansion so a big upsell
  cannot mask churn.

The retention metrics live at the seam where this reference meets
[retention](retention.md): the funnel books the win, and retention decides whether the
won revenue compounds or drains.

## Instrumenting deterministically

The metrics are only as trustworthy as the pipe they flow through. Three rules turn a
pile of tools into one source of truth.

1. **One source of truth.** The CRM holds the funnel. Stage, amount, owner, and
   timestamps live there and nowhere else. A spreadsheet that recomputes win rate by
   hand is a second source — and a second source is a future disagreement about what is
   true.
2. **One definition per metric.** Each metric has a written formula and the exact
   fields it reads, stored beside the dashboard. "Win rate" resolves to one query, not
   to whichever analyst ran it.
3. **One dashboard, refreshed on a schedule.** A single view shows stage counts,
   conversion rates, CAC, LTV:CAC, payback, pipeline coverage, win rate, and NRR. The
   dashboard reads the CRM directly; nobody retypes a number into a slide.

Determinism check: two people pulling the same metric on the same day get the same
value. When they do not, a definition is ambiguous or a second source exists — fix the
definition or kill the source before trusting the number.

## Lifecycle and handoff alignment

A deal dies in the gaps between functions, not inside them. Each handoff is a contract:
a defined trigger, an accepting owner, and a service-level agreement (SLA) on response
time.

| Handoff | Trigger | From → To | SLA |
|---------|---------|-----------|-----|
| Lead → MQL routing | Lead crosses the MQL threshold | Marketing → Sales | Routed to an owner within 1 business day |
| MQL → SQL acceptance | Sales works the MQL | Sales accepts or rejects with a reason | First touch within 1 business day; accept/reject within 3 |
| Won → onboarding | Contract signed | Sales → Success | Kickoff scheduled within 2 business days |
| Renewal/expansion | Renewal window opens | Success owns the motion | Renewal conversation opened 90 days out |

The contract that makes the first handoff hold is a shared MQL definition signed by
marketing and sales: marketing stops throwing volume over the wall, and sales stops
ignoring leads it privately deems weak. A rejected MQL returns a reason, and that
reason retunes the marketing score — the loop closes instead of festering.

## The tooling stack

Keep the stack to the smallest set that produces one trustworthy number.

- **CRM** (system of record): HubSpot, Salesforce, or Pipedrive. Holds stages, deals,
  owners, and timestamps. The CRM is the source of truth.
- **Product and revenue analytics**: a warehouse-backed BI tool (Metabase, Looker) or
  product analytics (Amplitude, PostHog) for cohort retention, NRR, and activation.
  Reads from the CRM and the product database.
- **Attribution**: first-touch and multi-touch models that tie pipeline back to
  channels. Honest attribution accepts that channels assist each other; it reports a
  range and its assumptions rather than a single tidy credit.

A founder does not need every category on day one. One CRM, one BI tool, and a
documented attribution model beat a dozen integrations nobody trusts.

## Failure modes

- **Vanity metrics.** Tracking totals that only rise — cumulative signups, raw traffic,
  total leads — instead of rates and unit economics. A number that cannot go down
  cannot inform a decision.
- **Inconsistent stage definitions.** "MQL" means a form fill to marketing and a
  budget-confirmed buyer to sales. Conversion rates computed across the seam are
  fiction, and the two teams blame each other for a measurement artifact.
- **No single source of truth.** The CRM, a spreadsheet, and the billing system each
  report a different MRR. Every meeting reconciles numbers instead of acting on them.
- **Attribution theater.** A model engineered to credit a favored channel, presented as
  fact. The spend follows the story, not the pipeline, and the real driver starves.
- **Pipeline inflation.** Stale opportunities with optimistic close dates left open to
  flatter coverage. The forecast misses because the pipeline was a wish.
- **Measuring activity, not outcomes.** Calls dialed and emails sent stand in for
  pipeline created and revenue booked. Activity is an input; rewarding it as an output
  breeds motion without progress.

## Red flags

- A metric on the board deck that no one can trace to a query.
- Marketing and sales reporting different counts for the same stage.
- Win rate computed including open opportunities.
- Pipeline coverage below 3× against the period target.
- LTV:CAC under 1:1, or a payback period over 18 months.
- NRR under 100% while the team chases new logos to paper over the leak.
- A loss with no recorded reason; a churn with no recorded reason.
- An attribution model that always credits the channel its owner runs.

## Worked example: LTV:CAC and payback

A founder of an early-stage SaaS pulls one quarter of numbers from the CRM and billing
system:

- Sales-and-marketing spend this quarter: **$60,000** (fully loaded).
- New customers won this quarter: **20**.
- Average revenue per customer: **$200 / month**.
- Gross margin: **75%**.
- Monthly churn rate: **2%** (so 2% of customers cancel each month).

**Step 1 — CAC.** Spend ÷ new customers = $60,000 ÷ 20 = **$3,000 per customer**.

**Step 2 — average lifetime.** 1 ÷ monthly churn = 1 ÷ 0.02 = **50 months**.

**Step 3 — LTV.** Monthly revenue × gross margin × lifetime = $200 × 0.75 × 50 =
**$7,500 per customer**.

**Step 4 — LTV:CAC.** LTV ÷ CAC = $7,500 ÷ $3,000 = **2.5:1**.

**Step 5 — payback period.** CAC ÷ (monthly revenue × gross margin) = $3,000 ÷ ($200 ×
0.75) = $3,000 ÷ $150 = **20 months**.

**Reading the result.** The 2.5:1 ratio sits just under the 3:1 SaaS benchmark — the
unit economics work, but with thin margin for rising acquisition costs. The 20-month
payback is the sharper warning: it exceeds the 12-month strong mark and the 18-month
strain line, so each customer ties up cash for nearly two years before repaying
acquisition. The lever is not "spend more on growth" — the lever is cut CAC or lift
margin and retention until payback drops under 18 months and the ratio clears 3:1.
Acting on the 2.5:1 without seeing the 20-month payback would fund growth the cash
balance cannot survive. The retention half of that lever is [the next stage of the
loop](retention.md): cutting churn lifts lifetime, which lifts LTV, which lifts this
ratio without spending a dollar more on acquisition.
