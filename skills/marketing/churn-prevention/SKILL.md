---
name: churn-prevention
description: Reduce customer churn and lift retention by diagnosing the driver behind each at-risk account, then matching the intervention to the cause. Use when churn or cancellations are rising, MRR is leaking, customers go quiet or stop logging in, payments fail, trials never activate, a save or win-back play is needed, or net revenue retention falls.
---

Cut churn the way a retention operator does: a cancellation is the lagging echo of
a decision the customer made weeks earlier, so the leverage is in the leading
signals, the segment, and the intervention matched to the driver. A discount is not
a diagnosis. Diagnose the cause, then choose the play that fits it.

Work the reference for the depth behind each step: [the retention playbook](references/retention-playbook.md).

## Steps

1. **Define churn and instrument the signals.** State the churn being addressed —
   voluntary (a decision) or involuntary (a failed payment) — and the period it
   covers. Stand up the four leading signals from the playbook: usage decay against
   the account baseline, failed payments, support sentiment, and unmet activation.
   This step is done when each of the four signals has a defined threshold and a
   data source, not a single MRR number.

2. **Segment the base by health.** Score every account into one bucket — at-risk,
   healthy, or power user — from the signals above, weighted into one health number.
   The activation rate belongs here as a retention metric, because an account that
   never reached first value was never retained. This step is done when each account
   carries exactly one segment and a health score that routes it.

3. **Diagnose the driver.** For an at-risk account, name the single cause behind the
   risk: stalled activation, usage decay, a stated intent to cancel, or a broken
   payment. The diagnosis is the routing key, so a wrong driver sends the wrong play.
   This step is done when each at-risk account carries one named driver backed by the
   signal that fired.

4. **Choose the intervention for that driver.** Match one play to the diagnosed
   driver: an onboarding nudge for stalled activation, a value reminder for usage
   decay, a save offer for a stated cancel, a win-back for an already-churned account,
   or a dunning sequence for a failed payment. Hold the discount as the last lever,
   reserved for confirmed price-driven churn. This step is done when each at-risk
   account is assigned one play whose trigger matches its driver.

5. **Measure with cohort-anchored metrics.** Track the outcome with gross revenue
   retention, net revenue retention, logo churn, and cohort retention curves read
   together — never a single blended average that hides the bleeding cohort. Tie each
   play to its own closing metric (activation fired, usage recovered, account stayed,
   account reactivated). This step is done when every play has a closing metric and
   the four portfolio metrics are reported side by side.

6. **Close the loop.** Record a structured exit reason on each cancellation in the
   period, and feed every confirmed driver back into the leading signals so the next
   occurrence routes faster. A release-driven decay on one account predicts the same
   on accounts sharing that release, so the driver becomes a new signal. This step is
   done when the latest cohort's drivers are recorded and the at-risk thresholds
   reflect them.
