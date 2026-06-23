# The Well-Architected Framework — six pillars applied

The Solutions Architect's review lenses for any AWS design. Six pillars frame every
workload; each takes a **named stance** before a resource is authored — a pillar with no
stance is a gap, not a default. The deterministic gates own syntax and formatting; this
page owns the architectural judgment they cannot encode.

Read the pillar in front of the decision you face. Each carries a decision procedure, the
failure modes that mark a weak design, the red flags that stop the line, and a worked
stance taken on the [managed-first reference architecture](managed-first.md#worked-example--a-managed-first-reference-architecture).

The pillars reinforce the managed-first default: the most managed service usually wins on
operational excellence, reliability, and sustainability at once, because the provider
already carries the patching, failover, and idle-capacity packing.

## 1. Operational excellence

Run the workload as code and observe it.

Decision procedure:

1. Express the infrastructure as code (Terraform or CDK), deployed through a pipeline in
   small, reversible changes.
2. Define the runbook for the top failure scenarios before launch.
3. Wire CloudWatch dashboards, metrics, and alarms a responder can act on — before the
   first incident, not after it.

Failure modes: console click-ops that leaves no diff; a deploy with no pipeline and no
rollback; an alarm storm nobody tuned; a runbook written after the outage.

Red flags: a resource in the console that does not exist in the IaC; no alarm on a new
failure path; a manual deploy step in the critical path.

## 2. Security

The pillar with the lowest tolerance for shortcuts; detailed in the
[security baseline](security-baseline.md).

Decision procedure:

1. Grant least privilege through IAM roles, never long-lived keys.
2. Encrypt at rest with KMS and in transit with TLS.
3. Close the network — private subnets, scoped security groups, no open admin ports.
4. Turn on the audit and detection trail: CloudTrail, Config, GuardDuty.

Failure modes: security deferred to a later "hardening pass"; a wildcard policy that turns
one compromised component into whole-account access; a public S3 bucket.

Red flags: `*` in an IAM `Action` or `Resource`; an unencrypted data store; a security
group opening `0.0.0.0/0` to a workload or admin port; CloudTrail off.

## 3. Reliability

Design for failure, because hardware and AZs do fail.

Decision procedure:

1. Span at least two Availability Zones for any stateful tier.
2. Add health checks and automated recovery (Auto Scaling, managed failover).
3. Prefer a managed service whose failover and backup AWS already operates.
4. Rehearse the restore path — a backup never tested is a backup that does not exist.

Failure modes: a single-AZ database; a recovery plan assumed rather than rehearsed; a
manual failover nobody has practiced.

Red flags: a stateful resource in one AZ; a backup with no tested restore; no health check
on a load-balanced target.

## 4. Performance efficiency

Pick the right resource shape and measure before tuning.

Decision procedure:

1. Choose the resource type the workload's measured profile needs, scaling horizontally
   where the work allows.
2. Prefer serverless and managed services that scale on demand over a hand-picked,
   always-on size.
3. Measure against the load curve, then tune — never tune on a guess.

Failure modes: an instance count picked by intuition; vertical scaling where horizontal
fits; optimization with no baseline measurement.

Red flags: a hand-picked fleet size with no load data; a single large instance where an
auto-scaling group belongs; tuning before a baseline exists.

## 5. Cost optimization

Pay for what the workload uses, and no more. This pillar holds the cost levers the
SKILL.md cost step pulls.

Decision procedure:

1. **Right-size** instances and storage classes to measured use; review Compute Optimizer
   and Cost Explorer on a cadence.
2. **Graviton** — choose ARM-based Graviton instances and Lambda for the price-performance
   gain where the runtime supports it.
3. **Commit and bid** — Savings Plans or Reserved capacity for steady workloads, Spot for
   fault-tolerant ones.
4. **Lifecycle** — S3 lifecycle rules to tier cold data to Infrequent Access then Glacier;
   schedule idle non-production resources off.
5. **Attribute** — a mandatory tag set so spend maps to an owner, and a Budget with an
   alert per account or workload.

Failure modes: an account with no budget; untagged resources nobody can attribute; an
oversized instance picked by guess; a dev environment running 24x7; cold data left on hot
storage.

Red flags: no AWS Budget on the account; a missing cost-allocation tag; on-demand pricing
for a year-round steady load; a non-production fleet with no off-hours schedule.

## 6. Sustainability

Minimize the energy behind the workload — which usually tracks cost downward too.

Decision procedure:

1. Minimize provisioned-but-idle capacity; prefer serverless and managed services that
   pack utilization across tenants.
2. Choose Graviton for its higher performance per watt.
3. Right-size storage and tier cold data so nothing spins that need not.

Failure modes: an over-provisioned always-on fleet for a spiky load; data kept hot forever;
x86 chosen where Graviton would do the same work for less energy.

Red flags: idle capacity held "just in case"; no lifecycle policy on growing storage; an
always-on fleet for a once-a-day job.

## The six-pillar review pass

Before a design is provisioned, walk all six and record the stance:

- **Operational excellence** — is it IaC, piped, and observable?
- **Security** — least-privilege, encrypted, closed, audited?
- **Reliability** — multi-AZ, recoverable, restore-tested?
- **Performance efficiency** — sized to measured load, scaling on demand?
- **Cost optimization** — budgeted, tagged, right-sized, committed/Spot, lifecycled?
- **Sustainability** — idle capacity minimized, Graviton where it fits?

A design that names no stance on a pillar is not done — that pillar is an unreviewed risk.

## Worked example — the six pillars on the reference architecture

The [managed-first reference architecture](managed-first.md#worked-example--a-managed-first-reference-architecture)
(Cognito → API Gateway → Lambda → DynamoDB / EventBridge → Aurora Serverless v2 → S3)
takes a stance on each pillar, and the managed-first choices satisfy several at once:

- **Operational excellence**: authored in CDK, deployed through a pipeline; CloudWatch
  alarms on Lambda errors and API Gateway 5xx wired before launch.
- **Security**: each Lambda assumes a scoped execution role (no keys); DynamoDB, Aurora,
  and S3 encrypt with KMS; the API enforces TLS; CloudTrail and GuardDuty are on. The full
  baseline is in [security-baseline.md](security-baseline.md).
- **Reliability**: every service is regional and multi-AZ by AWS default — DynamoDB, Aurora
  Serverless v2, and S3 carry failover and point-in-time recovery the team does not operate.
- **Performance efficiency**: Lambda and Aurora Serverless v2 scale on demand, so capacity
  follows the real load curve rather than a hand-picked size.
- **Cost optimization**: per-request billing idles at zero, an S3 lifecycle rule tiers cold
  archives to Glacier, a Budget with an alert guards the account, and the mandatory tag set
  attributes spend.
- **Sustainability**: serverless packs utilization and holds no idle fleet; Lambda runs on
  Graviton (`arm64`) for the performance-per-watt gain.

The single decision — choose the most managed service that meets the constraint — paid off
across operational excellence, reliability, cost, and sustainability together. The
remaining pillar work (the security baseline, the cost tags, the alarms) is wiring, not a
different architecture. The apply that makes any of it real is the approval-gated external
mutation governed by the [infra-safety discipline](../../../engineering/engineering/references/infra-safety.md)
and the foundation doctrine's [Genchi Genbutsu](../../../meta/foundation/SKILL.md).
