# Managed-first — the compute and data decision

The Cloud Architect's default move on Azure. The question on every component is not "how do
I run this?" but "what does Azure already run for me?" Prefer the service that removes the
most **undifferentiated heavy lifting** — patching, scaling, failover, backup, capacity
planning — and own a virtual machine only where a recorded constraint forces it. The
deterministic gates own syntax; this page owns the choice they cannot encode.

## The decision rule

**Choose the most managed option that meets the constraint.** Climb down the management
ladder only one rung at a time, and only when a written requirement from the workload rules
the rung above it out:

1. **Fully managed PaaS / serverless** — the platform runs everything; pay per request or
   per plan. Azure Functions, Container Apps, App Service, Azure SQL Database, Cosmos DB,
   Blob Storage, Service Bus, Event Grid.
2. **Managed orchestration / managed instances** — the platform runs the control plane; node
   sizing or instance sizing is yours. AKS, Azure SQL Managed Instance, a VM Scale Set
   behind a managed image.
3. **Self-managed on a VM** — a virtual machine is yours to patch, scale, back up, and
   monitor. The last resort, taken only against a named constraint.

A constraint is a written fact about the workload — a kernel module, a licensed engine, a
GPU-bound model, a Windows service that needs a real host, a sustained load where a reserved
VM is cheaper than per-request billing. "We've always run it on a box" is not a constraint.

## Compute — App Service vs Container Apps vs Functions vs AKS vs VM

| Dimension | Functions (serverless) | Container Apps (serverless containers) | App Service (managed web) | AKS (managed Kubernetes) | VM (self-managed) |
|---|---|---|---|---|---|
| Operational overhead | Lowest — no host, scales to zero | Low — no nodes, you ship a container | Low — managed web host, no OS | Medium — you own the cluster config and node pools | Highest — you own the OS, patching, scaling |
| Best fit | Event-driven, bursty, short tasks; glue | Microservices and event-driven containers; KEDA scaling | A web app or API, code or container, no orchestration need | A portfolio of services needing full Kubernetes control | A constraint the managed tiers cannot meet |
| Scaling | Automatic, per-event, to zero | Scale rules (HTTP, queue, KEDA), to zero | Autoscale by metric or schedule | Cluster autoscaler + HPA you configure | VM Scale Set you size and tune |
| Runtime limit | Consumption capped (extend on Premium) | Unbounded | Unbounded | Unbounded | Unbounded |
| Pricing shape | Per execution + GB-s; zero when idle | Per vCPU/GB-s while running; zero idle | Per plan (reserve the baseline) | Per node-hour, idle or not | Per VM-hour, idle or not |
| Reach for it when | The work is event-driven or bursty | The work is a container that should scale to zero | The work is a standard web app or API | A written need for full Kubernetes control | A kernel module, a license, a GPU, or a host-bound service |

Decision procedure for a compute component:

1. **Is the work event-driven, bursty, or a short task?** Azure Functions. Stop here.
2. **Is it a containerized service that should scale to zero** with no full-Kubernetes
   requirement? Container Apps. Stop here.
3. **Is it a standard web app or API** with no orchestration need? App Service (code or
   container). Stop here.
4. **Does a written requirement demand full Kubernetes control** (a service mesh, custom
   operators, a portfolio of interdependent services)? AKS, with the requirement recorded.
   Otherwise climb back to step 3.
5. **Does a constraint demand a real host** (a kernel module, a licensed engine, a GPU, a
   host-bound Windows service)? A VM in a Scale Set across zones, with the constraint
   recorded. Otherwise climb back to step 4.

Static Web Apps is a sixth option for a static or Jamstack front end with a managed API
backend; reach for it for a SPA or documentation site, and graduate to App Service when the
backend outgrows serverless functions.

## Data — Azure SQL vs Cosmos DB vs self-managed

| Dimension | Cosmos DB (serverless NoSQL) | Azure SQL Database (managed relational) | Azure SQL Managed Instance | Self-managed engine on a VM |
|---|---|---|---|---|
| Operational overhead | Lowest — no instances, autoscale RU/s | Low — managed engine, no OS | Medium — near-full SQL Server surface, managed host | Highest — you own engine, host, backups, failover |
| Data model | Document / key-value / graph / column | Relational (T-SQL) | Relational (near-full SQL Server compatibility) | Anything, at full operational cost |
| Scaling | Autoscale RU/s, per-request, global | vCore or DTU; elastic pools; read replicas | vCore; scoped to instance | Yours to build |
| Failover & backup | Built-in, multi-region, point-in-time | Built-in, failover groups, point-in-time | Built-in, failover groups | Yours to build and test |
| Reach for it when | Access is key/document-based or globally distributed | Relational with standard SQL needs | A lift of SQL Server needing instance-scoped features (SQL Agent, CLR, cross-DB) | A licensed/unusual engine the managed tiers cannot host |

Decision procedure for a data store:

1. **Is the access pattern document- or key-based, or globally distributed** with no
   relational-join requirement? Cosmos DB. Stop here.
2. **Does the workload need relational queries** on a standard SQL surface? Azure SQL
   Database. Stop here.
3. **Does a lift of SQL Server need instance-scoped features** (SQL Agent, CLR, cross-database
   queries) that Azure SQL Database does not expose? Azure SQL Managed Instance, with the
   feature recorded. Otherwise climb back to step 2.
4. **Does a constraint rule out the managed engines** (a licensed database, an engine Azure
   does not offer as a service, an extension the managed tier forbids)? A self-managed engine
   on a VM — zone-redundant, automated backups, and a rehearsed restore, with the constraint
   recorded. Otherwise climb back to step 3.

Cache and search are managed too: Azure Cache for Redis for an in-memory cache, Azure AI
Search for search and retrieval — never a Redis or Elasticsearch process hand-run on a VM
where the managed service fits.

## The serverless glue

A managed-first architecture stitches its components together with managed integration
services, not with polling loops and cron on a box:

- **Blob Storage** — object storage, the default home for files, backups, static assets, and
  data lakes; durable and effectively infinite, no capacity to plan.
- **Service Bus** — a managed broker with queues and topics to decouple producers from
  consumers and absorb bursts.
- **Event Grid** — an event router for reactive, event-driven wiring without point-to-point
  coupling.
- **Logic Apps** — managed workflow orchestration for a multi-step integration, replacing a
  hand-rolled state machine and its retry logic.
- **API Management** — a managed gateway in front of App Service, Functions, or Container
  Apps, replacing a self-run reverse proxy and handling throttling and auth.
- **Microsoft Entra ID** — managed identity, sign-up, and federation, replacing a hand-built
  auth service.

## Failure modes

The recurring ways a team reaches past the managed option and pays for it later:

- **Reflexive VM.** A virtual machine stood up because the team knows servers, where
  Functions, Container Apps, or App Service fits — now they own patching, scaling, and an
  on-call rotation Azure would have carried.
- **Reflexive AKS.** A Kubernetes cluster adopted for a single web service, where App Service
  or Container Apps carries it without a cluster to operate.
- **Self-managed database.** SQL Server or Postgres on a VM "for control" — the control is
  mostly nightly backup scripts, failover that has never been tested, and version upgrades
  nobody schedules.
- **Polling loop.** A cron job on a VM polling a blob container or a table every minute, where
  an Event Grid subscription or a Service Bus trigger would push the work and cost nothing
  while idle.
- **Hand-rolled auth.** A bespoke user store and password flow where Entra ID carries
  sign-up, MFA, and federation as a managed service.
- **Always-on for a batch.** A 24x7 VM for a job that runs once a day, where a scheduled
  Function or a Container Apps job billed per run would idle at zero.

## Red flags

A fast scan over a design — any one of these stops the line:

- A VM whose justification is habit, not a written constraint.
- An AKS cluster for a single service that App Service or Container Apps would run.
- A database engine hand-run on a VM where Azure SQL Database, Managed Instance, or Cosmos DB
  fits.
- A polling loop or cron-on-a-VM where an Event Grid or Service Bus trigger belongs.
- A self-built queue, scheduler, or auth service duplicating Service Bus, Logic Apps, or
  Entra ID.
- An always-on resource serving a spiky or once-a-day workload.

## Worked example — a PaaS-first reference architecture

A request-driven web API with a user store, an async processing path, and a relational
store, built so the team owns no virtual machine at all. Every box is a managed service; the
constraint that would force a VM never appears, so none is provisioned.

```
            ┌────────────┐
  client ─▶ │ Front Door │  managed edge: WAF, TLS, CDN cache
            └─────┬──────┘
                  │ routed request
            ┌─────▼──────────┐
            │ API Management │  managed gateway (throttling, authz via Entra ID)
            └─────┬──────────┘
                  │ forward
            ┌─────▼──────┐        ┌──────────────────────┐
            │ App Service│ ─────▶ │ Azure SQL Database    │  managed relational, zone-redundant
            │  (web/api) │        └──────────────────────┘
            └─────┬──────┘          (reached via managed identity)
                  │ publish message (no polling)
            ┌─────▼────────┐
            │ Service Bus  │  managed broker, decouples async work
            └─────┬────────┘
                  │ queue trigger
            ┌─────▼──────┐        ┌──────────────┐
            │ Functions  │ ─────▶ │ Blob Storage │  durable object store + lifecycle tiering
            │  (worker)  │        └──────────────┘
            └────────────┘
```

Why each rung was chosen, against the decision procedures above:

- **Compute (web/api)** stops at App Service: the work is a standard HTTP API with no
  orchestration need, so the procedure stops at step 3 — no AKS cluster, no VM. App Service
  carries the OS, patching, and autoscale.
- **Compute (worker)** stops at Azure Functions: the async path is event-driven, triggered by
  a Service Bus message, and bills at zero when idle, so the procedure stops at step 1.
- **Relational data** is Azure SQL Database because the API needs standard relational queries
  with no instance-scoped SQL Server feature — the procedure stops at step 2, no Managed
  Instance and no self-managed engine.
- **Integration** is Service Bus, not a polling loop — App Service publishes a message and the
  broker triggers the worker, so the worker costs nothing until there is work.
- **Identity** is Entra ID and the **gateway** is API Management — both managed, so no auth
  service and no reverse proxy are hand-run; App Service and Functions reach SQL and Blob
  Storage through managed identities.
- **Edge** is Front Door with WAF and CDN caching, and **archive** is Blob Storage with a
  lifecycle rule tiering cold blobs to Cool then Archive — durability and cost optimization
  with no storage capacity to plan.

Authoring this in Bicep or Terraform and reading the plan before any deploy is the rest of
the discipline: see the [governance-and-identity baseline](governance-and-identity.md) for
the Entra ID, RBAC, encryption, and network posture each box still needs, and the
[Well-Architected review](well-architected.md) for the five-pillar pass before it is
provisioned. The deploy is the approval-gated external mutation, governed by the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
