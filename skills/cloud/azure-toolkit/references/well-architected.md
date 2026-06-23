# The Well-Architected Framework — five pillars applied

The Cloud Architect's review lenses for an Azure design. Five pillars frame the
workload; each takes a **named stance** before a resource is authored — a pillar with no
stance is a gap, not a default. The deterministic gates own syntax and formatting; this
page owns the architectural judgment they cannot encode.

Read the pillar in front of the decision you face. Each carries a decision procedure, the
failure modes that mark a weak design, the red flags that stop the line, and a worked
stance taken on the [PaaS-first reference architecture](managed-first.md#worked-example--a-paas-first-reference-architecture).

The pillars reinforce the PaaS-first default: the most managed service usually wins on
reliability, operational excellence, and cost at once, because the platform already
carries the patching, failover, and idle-capacity packing. The pillar order below follows
Microsoft's own — reliability leads — but security is the pillar that cannot be retrofitted
cheaply, so it leads the *design* even when it is listed second.

## 1. Reliability

Design for the failure that will happen, because regions, zones, and instances do fail.

Decision procedure:

1. Span availability zones across the stateful tier — zone-redundant Azure SQL,
   zone-redundant storage, an App Service plan or AKS node pool across zones.
2. Add health probes and automated recovery (App Service health check, AKS liveness probes,
   managed failover groups for Azure SQL).
3. Prefer a managed service whose failover and backup Azure already operates over a tier you
   recover by hand.
4. Rehearse the restore path against a written RTO and RPO — a backup never restored is a
   backup that does not exist.

Failure modes: a single-region single-instance workload sold as a cost saving; a recovery
objective assumed rather than measured; a failover nobody has practiced; a backup with no
tested restore.

Red flags: a stateful resource in one zone with no redundancy; a production workload with no
recovery objective written down; a backup with no tested restore; no health probe on a
load-balanced tier.

## 2. Security

Assume breach. The pillar with the lowest tolerance for shortcuts; the identity, network,
and encryption baseline is detailed in the
[governance-and-identity reference](governance-and-identity.md).

Decision procedure:

1. Authenticate through Microsoft Entra ID with a managed identity, never a shared secret or
   connection string.
2. Grant least privilege through scoped RBAC role assignments at the narrowest scope.
3. Encrypt at rest (platform keys by default, customer-managed keys in Key Vault for
   regulated data) and in transit (TLS 1.2 or higher, HTTPS-only).
4. Close the network — private endpoints, public network access disabled, NSGs with a
   default deny, no open admin port.
5. Turn on the detection trail: Defender for Cloud, diagnostic settings to Log Analytics,
   activity-log alerts on privileged operations.

Failure modes: security deferred to a later "hardening pass"; an `Owner` assignment that
turns one compromised principal into whole-subscription access; a storage account open to
the internet; a secret in app settings.

Red flags: `Owner` at subscription or management-group scope on a non-human principal;
public network access enabled on a storage account, SQL server, Cosmos account, or Key
Vault; a secret or connection string in code or config; an NSG opening `0.0.0.0/0` to port
22 or 3389; Defender for Cloud off.

## 3. Cost optimization

Pay for what the workload needs at the SKU it needs, and no more. This pillar holds the cost
levers the SKILL.md cost step pulls.

Decision procedure:

1. **Right-size** compute and storage to measured use; review Azure Advisor cost
   recommendations on a cadence.
2. **Commit** steady baseline load to one- or three-year reservations or a savings plan;
   keep spiky load on consumption or spot.
3. **Schedule and deallocate** — shut non-production environments down outside working hours;
   deallocate idle VMs rather than leaving them billing.
4. **Tier** — move cold blob data to Cool then Archive access tiers with a lifecycle
   management rule.
5. **Attribute** — a mandatory tag set (owner, environment, cost-center) on every resource
   group so spend maps to an owner, and an Azure budget with an alert per subscription or
   resource group.

Failure modes: a subscription with no budget; untagged resources nobody can attribute; an
oversized SKU picked by guess; a dev environment running 24x7; cold data left on the Hot
access tier; consumption pricing for a year-round steady load.

Red flags: no Azure budget on the subscription; a missing cost-allocation tag; pay-as-you-go
pricing for a steady baseline that a reservation would discount; a non-production resource
with no off-hours schedule.

## 4. Operational excellence

Run the workload as code and observe it in production.

Decision procedure:

1. Express the infrastructure as code (Bicep or Terraform), deployed through a pipeline in
   small, reversible changes.
2. Define the runbook for the top failure scenarios before launch.
3. Wire Azure Monitor metrics, Log Analytics queries, and alerts a responder can act on —
   before the first incident, not after it.

Failure modes: portal click-ops that leaves no diff; a deploy with no pipeline and no
rollback; an alert storm nobody tuned; a runbook written after the outage.

Red flags: a resource in the portal that does not exist in the IaC; no alert on a new
failure path; a manual deploy step in the critical path; diagnostic settings unset on a
resource.

## 5. Performance efficiency

Match the service and SKU to the load curve, and measure before tuning.

Decision procedure:

1. Choose the service and SKU the workload's measured profile needs, scaling out before
   scaling up where the service allows.
2. Prefer managed services that autoscale on demand (App Service autoscale, Container Apps
   scale rules, Cosmos DB autoscale RU/s) over a hand-picked, always-on size.
3. Cache the hot path (Azure Cache for Redis, CDN / Front Door) rather than recomputing it.
4. Measure against the load curve, then tune — never tune on a guess.

Failure modes: an instance count picked by intuition; vertical scaling where horizontal
fits; the hot path recomputed on every request; optimization with no baseline measurement.

Red flags: a hand-picked SKU with no load data; a single large instance where an autoscale
rule belongs; no cache on a read-heavy hot path; tuning before a baseline exists.

## The five-pillar review pass

Before a design is provisioned, walk all five and record the stance:

- **Reliability** — zone-redundant, recoverable, restore-tested against an RTO/RPO?
- **Security** — managed-identity, least-privilege, encrypted, private, detected?
- **Cost optimization** — budgeted, tagged, right-sized, committed, scheduled, tiered?
- **Operational excellence** — IaC, piped, and observable?
- **Performance efficiency** — sized to measured load, scaling on demand, hot path cached?

A design that names no stance on a pillar is not done — that pillar is an unreviewed risk.

## Worked example — the five pillars on the reference architecture

The [PaaS-first reference architecture](managed-first.md#worked-example--a-paas-first-reference-architecture)
(Front Door → App Service → Azure SQL Database, with Service Bus → Functions → Blob Storage
for the async path) takes a stance on each pillar, and the PaaS-first choices satisfy
several at once:

- **Reliability**: the App Service plan and Azure SQL Database deploy zone-redundant; a SQL
  failover group carries cross-region recovery; Blob Storage is geo-redundant (GRS); the RTO
  and RPO are written down and the restore is rehearsed in staging.
- **Security**: App Service and the Functions app each carry a system-assigned managed
  identity and reach Azure SQL and Blob Storage through it — no connection string; Azure SQL,
  the storage account, and Service Bus expose private endpoints with public network access
  disabled; Defender for Cloud is on. The full baseline is in
  [governance-and-identity.md](governance-and-identity.md).
- **Cost optimization**: the App Service plan reserved-instance discount covers the steady
  baseline; Functions run on the consumption plan and idle at zero; a lifecycle rule tiers
  cold blobs to Cool then Archive; an Azure budget with an alert guards the subscription; the
  mandatory tag set attributes spend.
- **Operational excellence**: authored in Bicep, deployed through a pipeline; Azure Monitor
  alerts on App Service 5xx and Functions failures wired before launch.
- **Performance efficiency**: App Service autoscale and Cosmos-style demand scaling follow
  the real load curve; Front Door caches static content at the edge so the hot path is not
  recomputed on every request.

The single decision — choose the most managed service that meets the constraint — paid off
across reliability, cost, and operational excellence together. The remaining pillar work
(the managed-identity wiring, the cost tags, the alerts) is wiring, not a different
architecture. The deploy that makes any of it real is the approval-gated external mutation
governed by the [infra-safety discipline](../../../engineering/engineering/references/infra-safety.md)
and the foundation doctrine's [Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the
real plan, never assume it.
