# The Architecture Framework — five categories applied

The GCP architect's review lenses over a Google Cloud design. Google's Architecture
Framework names five categories; each takes a **named stance** before a resource is
authored — a category with no stance is a gap, not a default. The deterministic gates own
syntax and formatting; this page owns the architectural judgment they cannot encode.

Read the category in front of the decision you face. Each category carries a decision
procedure, the failure modes that mark a weak design, the red flags that stop the line,
and a worked stance taken on the
[serverless-first reference architecture](managed-first.md#worked-example--a-serverless-first-reference-architecture).

The categories reinforce the serverless-first default: the most managed service usually
wins on operational excellence, reliability, and cost at once, because Google already
carries the patching, the failover, and the scale-to-zero idle packing.

## 1. Operational excellence

Run the workload as code, observe it, and rehearse its incidents.

Decision procedure:

1. Express the infrastructure as code (Terraform or Config Connector), deployed through a
   pipeline in small, reversible changes.
2. Write the runbook for the top failure scenarios before launch.
3. Wire Cloud Monitoring dashboards, metrics, and alerts a responder can act on — before
   the first incident, not after it.

Failure modes: console click-ops that leaves no diff; a deploy with no pipeline and no
rollback; an alert storm nobody tuned; a runbook written after the outage.

Red flags: a resource in the console that does not exist in the IaC; no alert on a new
failure path; a manual deploy step in the critical path.

## 2. Security, privacy, and compliance

The category with the lowest tolerance for shortcuts; the resource hierarchy, IAM, CMEK,
and network posture are detailed in the [IAM and SRE reference](iam-and-sre.md).

Decision procedure:

1. Place the workload in its own project under the right folder, so the project is the
   isolation boundary and org policy inherits down to it.
2. Grant least privilege through service accounts bound to predefined or custom roles via
   Workload Identity, never a downloaded JSON key.
3. Encrypt at rest with customer-managed keys (CMEK) through Cloud KMS, and in transit with
   TLS.
4. Close the network — custom-mode VPC, default-deny firewall, Private Google Access, no
   public IP on a data store.
5. Turn on the audit trail — Cloud Audit Logs (Admin Activity and Data Access) and Security
   Command Center.

Failure modes: security deferred to a later hardening pass; a primitive role that turns one
compromised principal into project-wide access; a public Cloud Storage bucket; a downloaded
service-account key that never expires.

Red flags: `roles/owner` or `roles/editor` on a human or an automation account; an
unencrypted data store where compliance demands CMEK; a firewall opening `0.0.0.0/0` to a
management port; Data Access logs off on a project holding regulated data.

## 3. Reliability

Design for the failure of a zone or a dependency, because zones and dependencies do fail.
The reliability discipline is Google's own SRE practice — SLOs and error budgets — set out
in the [SRE section](iam-and-sre.md#sre-slos-and-error-budgets).

Decision procedure:

1. Set an SLO for the critical user journey, and derive the error budget from it.
2. Span more than one zone across the stateful tier; pick multi-region by the SLO the
   journey demands.
3. Prefer a managed service whose failover and backup Google already operates.
4. Rehearse the restore path — a backup never restored is a backup that does not exist.

Failure modes: a single-zone database; a reliability target nobody measures; a recovery
plan assumed rather than rehearsed; a release that ignores a spent error budget.

Red flags: a stateful resource in one zone; a service with no SLO; a backup with no tested
restore; a deploy that proceeds while the error budget is exhausted.

## 4. Cost optimization

Pay for what the workload uses, and no more. This category holds the cost levers the
SKILL.md cost step pulls.

Decision procedure:

1. **Right-size and scale to zero** — act on the Recommender's right-sizing output, and
   prefer services (Cloud Run, Cloud Functions) that bill at zero while idle.
2. **Commit the steady baseline** — committed-use discounts (CUDs) for predictable
   compute, reserved for the flat baseline rather than the spiky peak.
3. **Tier and lifecycle storage** — Cloud Storage lifecycle rules to move cold objects to
   Nearline, Coldline, then Archive; schedule idle non-production resources off.
4. **Attribute** — a mandatory label set so spend maps to an owner, and a billing budget
   with an alert threshold per project or billing account.

Failure modes: a billing account with no budget; unlabeled resources nobody can attribute;
an oversized VM picked by guess; a dev environment running 24x7; cold data left on Standard
storage.

Red flags: no billing budget on a production billing account; a missing cost-allocation
label; on-demand pricing for a year-round steady load; a non-production resource with no
off-hours schedule.

## 5. Performance optimization

Size and place the workload to the measured load, then tune.

Decision procedure:

1. Choose the resource shape the workload's measured profile needs, scaling horizontally
   where the work allows.
2. Prefer serverless and managed services that autoscale on demand over a hand-picked,
   always-on size.
3. Place data near compute — co-locate the store and the service in the region the users
   sit closest to.
4. Measure against the latency or throughput budget, then tune — never tune on a guess.

Failure modes: an instance count picked by intuition; a store in one region and its
compute in another; vertical scaling where horizontal fits; optimization with no baseline.

Red flags: a hand-picked fleet size with no load data; cross-region latency between a
service and its store; tuning before a baseline exists.

## The five-category review pass

Before a design is provisioned, walk all five and record the stance:

- **Operational excellence** — is it IaC, piped, and observable?
- **Security, privacy, and compliance** — project-isolated, least-privilege, CMEK-encrypted,
  closed, audited?
- **Reliability** — does it carry an SLO, an error budget, multi-zone, and a tested restore?
- **Cost optimization** — budgeted, labeled, right-sized, committed, lifecycled?
- **Performance optimization** — sized to measured load, data near compute, scaling on demand?

A design that names no stance on a category is not done — that category is an unreviewed
risk. Severity follows
[the review lenses](../../../engineering/code-review/references/review-lenses.md): a public
bucket, a primitive role on automation, or a downloaded key is a **blocker**; a missing SLO
or absent Data Access logs is a **major**; an unlabeled non-production resource is a
**minor**. Tie each finding to the category it endangers.

## Worked example — the five categories on the reference architecture

The [serverless-first reference architecture](managed-first.md#worked-example--a-serverless-first-reference-architecture)
(Identity Platform → API Gateway → Cloud Run → Firestore / Pub/Sub → Cloud Run worker →
Cloud SQL → Cloud Storage) takes a stance on each category, and the serverless-first
choices satisfy several at once:

- **Operational excellence**: authored in Terraform, deployed through Cloud Build; Cloud
  Monitoring alerts on Cloud Run error rate and request latency wired before launch.
- **Security, privacy, and compliance**: the stack lives in its own project under the
  `prod` folder; each Cloud Run service runs as its own service account via Workload
  Identity (no key); Firestore, Cloud SQL, and Cloud Storage encrypt with CMEK; the API
  enforces TLS; Cloud Audit Logs and Security Command Center are on. The full baseline is
  in [iam-and-sre.md](iam-and-sre.md).
- **Reliability**: the critical journey carries a 99.9% availability SLO with a burn-rate
  alert; every service is regional and multi-zone by Google default — Firestore, Cloud SQL
  (regional HA), and Cloud Storage carry failover and point-in-time recovery the team does
  not operate.
- **Cost optimization**: Cloud Run and Cloud Functions bill at zero when idle; a Cloud
  Storage lifecycle rule tiers cold archives to Coldline then Archive; a billing budget
  with an alert guards the project; the mandatory label set attributes spend; CUDs cover
  the Cloud SQL baseline.
- **Performance optimization**: Cloud Run autoscales on request load, so capacity follows
  the real curve; Firestore and Cloud SQL sit in the same region as the services, so no
  cross-region hop sits on the critical path.

The single decision — choose the most managed service that meets the constraint — paid off
across operational excellence, reliability, cost, and performance together. The remaining
work (the CMEK keys, the cost labels, the alerts) is wiring, not a different architecture.
The apply that makes any of it real against a live project is the approval-gated external
mutation governed by the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
