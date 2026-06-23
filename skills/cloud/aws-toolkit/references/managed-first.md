# Managed-first — the compute and data decision

The Solutions Architect's default move. The question on every component is not "how do I
run this?" but "what does AWS already run for me?" Prefer the service that removes the
most **undifferentiated heavy lifting** — patching, scaling, failover, backup, capacity
planning — and own a server only where a recorded constraint forces it. The deterministic
gates own syntax; this page owns the choice they cannot encode.

## The decision rule

**Choose the most managed option that meets the constraint.** Climb down the management
ladder only one rung at a time, and only when a written requirement from the workload
rules the rung above it out:

1. **Fully managed / serverless** — the provider runs everything; pay per request or per
   unit of work. Lambda, Fargate, DynamoDB, Aurora Serverless v2, S3, SQS, EventBridge.
2. **Managed instances** — the provider runs the engine and the host; sizing is yours.
   RDS, ElastiCache, OpenSearch, MSK, an EC2 Auto Scaling group behind a managed AMI.
3. **Self-managed on EC2** — a server is yours to patch, scale, back up, and monitor. The
   last resort, taken only against a named constraint.

A constraint is a written fact about the workload — a kernel module, a licensed engine, a
sub-millisecond budget, a sidecar that needs a real host, a sustained load where a server
is cheaper than per-request billing. "We've always run it on a box" is not a constraint.

## Compute — Lambda vs Fargate vs EC2

| Dimension | Lambda (serverless) | Fargate (serverless containers) | EC2 (self-managed) |
|---|---|---|---|
| Operational overhead | Lowest — no host, no scaling to manage | Low — no nodes, you ship a container | Highest — you own the host, patching, scaling |
| Best fit | Event-driven, spiky, short tasks; glue between services | Long-running or steady containerized services; existing Docker images | A constraint the managed tiers cannot meet |
| Scaling | Automatic, per-request, to zero | Task count scales; no node pool | Auto Scaling group you size and tune |
| Runtime limit | 15-minute max execution | Unbounded | Unbounded |
| Pricing shape | Per request + GB-second; zero when idle | Per vCPU/GB-second while running | Per instance-hour, idle or not |
| Reach for it when | The work is event-driven or bursty | The work is a steady container without a host constraint | A kernel module, a special instance type, a license, or a GPU-bound workload forces a host |

Decision procedure for a compute component:

1. **Is the work event-driven, bursty, or under 15 minutes?** Lambda. Stop here.
2. **Is it a long-running container with no host-level constraint?** Fargate. Stop here.
3. **Does a written constraint demand a real host** (kernel access, a licensed engine,
   a specialized instance family, a GPU)? EC2 in an Auto Scaling group across two AZs,
   with the constraint recorded. Otherwise climb back to step 2.

App Runner is a fourth option for a stateless HTTP container that wants Fargate's freedom
from hosts with even less wiring (no load balancer or task definition to author); reach
for it for a simple web service or API, and graduate to Fargate when networking or sidecar
needs outgrow it.

## Data — DynamoDB vs Aurora vs RDS vs self-managed

| Dimension | DynamoDB (serverless KV) | Aurora Serverless v2 | RDS (managed instance) | Self-managed DB on EC2 |
|---|---|---|---|---|
| Operational overhead | Lowest — no instances, no patching | Low — managed engine, capacity auto-scales | Medium — you size the instance | Highest — you own engine, host, backups, failover |
| Data model | Key-value / document | Relational (PostgreSQL / MySQL wire-compatible) | Relational (Postgres, MySQL, others) | Anything, at full operational cost |
| Scaling | Automatic, per-request, to zero | Capacity units auto-scale to load | Manual resize / read replicas | Yours to build |
| Failover & backup | Built-in, multi-AZ, point-in-time | Built-in, multi-AZ | Built-in (Multi-AZ option) | Yours to build and test |
| Reach for it when | Access patterns are known and key-based | Relational + spiky or unpredictable load | Relational + steady, predictable load | A licensed/unusual engine or a constraint RDS cannot host |

Decision procedure for a data store:

1. **Is the access pattern key-based with known queries** (no ad-hoc joins)? DynamoDB.
   Stop here.
2. **Does the workload need relational queries?** Then choose by load shape:
   - Spiky or unpredictable load — Aurora Serverless v2 (capacity follows demand).
   - Steady, predictable load — RDS (or provisioned Aurora) sized to the curve.
3. **Does a constraint rule out the managed engines** (a licensed database, an engine AWS
   does not offer, an extension RDS forbids)? Self-managed on EC2 — Multi-AZ, automated
   backups, and a rehearsed restore, with the constraint recorded. Otherwise climb back to
   step 2.

Cache and search are managed too: ElastiCache (Redis/Memcached) for an in-memory cache,
OpenSearch Service for search and log analytics — never a Redis or Elasticsearch process
hand-run on EC2 where the managed service fits.

## The serverless glue

A managed-first architecture stitches its components together with managed integration
services, not with polling loops and cron on a box:

- **S3** — object storage, the default home for files, backups, static assets, and data
  lakes; durable and effectively infinite, no capacity to plan.
- **SQS** — a managed queue to decouple producers from consumers and absorb bursts.
- **SNS / EventBridge** — pub/sub and an event bus to route work without point-to-point
  coupling; EventBridge for event-driven routing, SNS for fan-out notification.
- **Step Functions** — managed orchestration for a multi-step workflow, replacing a
  hand-rolled state machine and its retry logic.
- **Cognito** — managed user identity, sign-up, and federation, replacing a hand-built
  auth service.
- **API Gateway / ALB** — a managed front door for Lambda or Fargate, replacing a
  self-run reverse proxy.

## Failure modes

The recurring ways a team reaches past the managed option and pays for it later:

- **Reflexive EC2.** A fleet stood up because the team knows servers, where Lambda or
  Fargate fits — now they own patching, scaling, and an on-call rotation AWS would have
  carried.
- **Self-managed database.** Postgres on EC2 "for control" — the control is mostly nightly
  backup scripts, failover that has never been tested, and version upgrades nobody schedules.
- **Polling loop.** A cron job on an instance polling S3 or a table every minute, where an
  S3 event or EventBridge rule would push the work and cost nothing while idle.
- **Hand-rolled auth.** A bespoke user store and password flow where Cognito carries
  sign-up, MFA, and federation as a managed service.
- **Always-on for a batch.** A 24x7 instance for a job that runs once a day, where a
  scheduled Lambda or a Fargate task billed per run would idle at zero.
- **Lift-and-shift frozen.** A VM-shaped app moved onto EC2 and never decomposed, so it
  never picks up any managed service it could have.

## Red flags

A fast scan over a design — any one of these stops the line:

- An EC2 instance whose justification is habit, not a written constraint.
- A database engine hand-run on a host where RDS, Aurora, or DynamoDB fits.
- A polling loop or cron-on-a-box where an event source belongs.
- A self-built queue, scheduler, or auth service duplicating SQS, EventBridge, or Cognito.
- An always-on resource serving a spiky or once-a-day workload.
- A "control" argument for a server with no named capability the managed tier lacks.

## Worked example — a managed-first reference architecture

A request-driven web API with a user store, an async processing path, and a relational
store, built so the team owns no server at all. Every box is a managed service; the
constraint that would force a server never appears, so none is provisioned.

```
            ┌────────────┐
  client ─▶ │  Cognito   │  managed identity: sign-up, MFA, federation
            └─────┬──────┘
                  │ authenticated request
            ┌─────▼──────┐
            │ API Gateway│  managed front door (HTTP, throttling, authz)
            └─────┬──────┘
                  │ invoke
            ┌─────▼──────┐        ┌──────────────┐
            │   Lambda   │ ─────▶ │  DynamoDB    │  serverless KV, scales to zero
            │  (handler) │        └──────────────┘
            └─────┬──────┘
                  │ publish event (no polling)
            ┌─────▼────────┐
            │ EventBridge  │  managed event bus, routes async work
            └─────┬────────┘
                  │ rule → target
            ┌─────▼──────┐        ┌──────────────────────┐
            │   Lambda   │ ─────▶ │ Aurora Serverless v2  │  relational, spiky load
            │  (worker)  │        └──────────────────────┘
            └─────┬──────┘
                  │ archive
            ┌─────▼──────┐
            │     S3     │  durable object store + lifecycle to cheaper tiers
            └────────────┘
```

Why each rung was chosen, against the decision procedures above:

- **Compute** stops at Lambda for both the synchronous handler and the async worker: the
  work is request-driven and event-driven, under the 15-minute limit, and bills at zero
  when idle. No host constraint appears, so the procedure never descends to Fargate or EC2.
- **Primary data** is DynamoDB because the API's access is key-based with known queries —
  the procedure stops at rung 1, no relational engine needed.
- **Relational data** for the async path is Aurora Serverless v2: the path needs joins and
  the load is spiky, so capacity follows demand rather than a hand-picked instance running
  24x7.
- **Integration** is EventBridge, not a polling loop — the handler publishes an event and
  the bus routes it, so the worker costs nothing until there is work.
- **Identity** is Cognito and the **front door** is API Gateway — both managed, so no auth
  service and no reverse proxy are hand-run.
- **Archive** is S3 with a lifecycle rule tiering cold objects to Infrequent Access and
  then Glacier — durability and cost optimization with no storage capacity to plan.

Authoring this in Terraform or CDK and reading the plan before any apply is the rest of the
discipline: see the [security baseline](security-baseline.md) for the IAM, encryption, and
network posture each box still needs, and the [Well-Architected review](well-architected.md)
for the six-pillar pass before it is provisioned. The apply is the approval-gated external
mutation, governed by the [infra-safety discipline](../../../engineering/engineering/references/infra-safety.md)
and grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
