---
name: revops
description: Build a founder's revenue engine — define one funnel, instrument the metrics from a single source of truth, align the marketing-sales-success handoffs, and run the pipeline on a cadence. Use when the user asks to set up revenue operations, design a funnel, define lead/MQL/SQL/pipeline stages, compute CAC, LTV, LTV:CAC, payback, win rate, or NRR, fix inconsistent funnel metrics, or align marketing and sales handoffs.
---

Revenue operations makes a founder's revenue predictable: one funnel every
function reads the same way, metrics computed from a single source of truth, and
handoffs that lose no deal between marketing, sales, and success. The leverage is
a number a founder can forecast against — not another dashboard.

A funnel a founder cannot reason about is worse than none: a false number drives a
false decision. Spend the judgment once, when the stage definitions are set, so
every later read is mechanical. The full standard — stage definitions, metric
formulas, tooling, failure modes, and a worked example — lives in
[references/revenue-operations.md](references/revenue-operations.md).

## Steps

1. **Define the funnel stages.** Write one entry condition per stage across the
   eight named stages — lead, MQL, SQL, opportunity, closed-won, closed-lost,
   expansion, churn — using the table in
   [references/revenue-operations.md](references/revenue-operations.md). An entry
   condition is observable in the CRM, not a feeling. Done when the eight stages
   each carry one binary entry condition and one named owner.

2. **Instrument the metrics from one source of truth.** Designate the CRM as the
   system of record, then write each metric's formula and the exact fields it
   reads beside the dashboard: CAC, LTV, LTV:CAC, payback, per-stage conversion,
   win rate, pipeline coverage, and NRR. Done when two people pulling the same
   metric on the same day get the same value.

3. **Set the targets.** Attach a target to each metric: LTV:CAC at or above 3:1,
   payback under 18 months, pipeline coverage at 3× to 4× of the period revenue
   goal, and a stage-conversion target per adjacent pair. Done when every tracked
   metric has a written target and a current value beside it.

4. **Find the bottleneck stage.** Compare each stage-conversion rate against its
   target and rank the gaps; the largest shortfall against target is the
   constraint. Done when one stage is named the bottleneck and its conversion gap
   is quantified.

5. **Align the handoffs.** Assign each handoff a trigger, an accepting owner, and
   a response-time SLA, per the handoff table in
   [references/revenue-operations.md](references/revenue-operations.md); the
   lead→MQL→SQL seam rests on an MQL definition signed by marketing and sales.
   Done when every handoff has an owner and an SLA, and a rejected MQL returns a
   reason that retunes the score.

6. **Review on a cadence.** Set a recurring review that reads the dashboard
   directly, walks the funnel top to bottom, and reconfirms the bottleneck from
   step 4 against fresh numbers. Done when the review is scheduled and its first
   run has recorded one owned action on the bottleneck stage.
