# Serverless-first — the compute and data decision

The GCP architect's default move. The question on every component is not "how do I run
this?" but "what does Google already run for me, and which option scales to zero?" Prefer
the service that removes the most **undifferentiated work** — patching, node management,
scaling, failover, backup, capacity planning — and own a VM only where a recorded
constraint forces it. The deterministic gates own syntax; this page owns the choice they
cannot encode.

## The decision rule

**Choose the most managed option that meets the constraint.** Climb down the management
ladder one rung at a time, and only against a written requirement from the workload that
rules the rung above it out:

1. **Serverless / fully managed** — Google runs everything and the bill drops to zero while
   idle. Cloud Run, Cloud Functions, Firestore, BigQuery, Cloud Storage, Pub/Sub.
2. **Managed nodes / managed instances** — Google runs the control plane or the engine; some
   sizing is yours. GKE Autopilot, Cloud SQL, Memorystore, a managed instance group.
3. **Self-managed on Compute Engine** — a VM is yours to patch, scale, back up, and monitor.
   The last resort, taken only against a named constraint.

A constraint is a written fact about the workload — a daemon that needs a real host, a
licensed engine, a GPU pinned to a node, a sustained load where a reserved VM is cheaper
than per-request billing, a sidecar that the serverless runtime cannot host. "We have
always run it on a box" is not a constraint.

## Compute — Cloud Run vs GKE Autopilot vs Cloud Functions vs Compute Engine

| Dimension | Cloud Run (serverless containers) | Cloud Functions (serverless FaaS) | GKE Autopilot (managed K8s) | Compute Engine (self-managed) |
|---|---|---|---|---|
| Operational overhead | Lowest — no host, scales to zero | Lowest — no host, per-event | Low — no node ops, you ship pods | Highest — you own the host, patching, scaling |
| Best fit | Stateless HTTP services, APIs, jobs; any container | Event-driven glue, a single function | A Kubernetes workload: many services, operators, a service mesh | A constraint the managed tiers cannot meet |
| Scaling | Automatic, per-request, to zero | Automatic, per-event, to zero | Pod autoscaling; pay per pod resource | Managed instance group you size and tune |
| Packaging | A container image | A function (source or container) | Kubernetes manifests | An OS image you build and patch |
| Pricing shape | Per request + CPU/memory time; zero idle | Per invocation + compute time; zero idle | Per pod vCPU/memory while running | Per VM-hour, idle or not |
| Reach for it when | The work is a stateless container | The work is one event-driven function | The team already runs Kubernetes and needs its primitives | A kernel module, a GPU-pinned host, a licensed daemon forces a VM |

Decision procedure for a compute component:

1. **Is the work a single event-driven function** (a Pub/Sub trigger, a Cloud Storage
   event, an HTTP webhook)? Cloud Functions. Stop here.
2. **Is the work a stateless container or HTTP service** with no Kubernetes-specific need?
   Cloud Run. Stop here.
3. **Does the workload genuinely need Kubernetes primitives** (operators, a service mesh,
   many co-scheduled services, custom resource definitions)? GKE Autopilot, so Google runs
   the nodes. Otherwise climb back to step 2.
4. **Does a written constraint demand a real VM** (kernel access, a GPU pinned to a host, a
   licensed daemon, a specialized machine family)? Compute Engine in a managed instance
   group across two zones, with the constraint recorded. Otherwise climb back to step 3.

GKE Autopilot is the managed-node default over GKE Standard: Google manages the nodes,
the autoscaling, and the security posture, so the team owns the workload and not the fleet.
Reach for GKE Standard only against a recorded need for node-level control that Autopilot
withholds.

## Data — Firestore vs Cloud SQL vs Spanner vs BigQuery

| Dimension | Firestore (serverless document) | Cloud SQL (managed relational) | Spanner (global relational) | BigQuery (serverless warehouse) |
|---|---|---|---|---|
| Operational overhead | Lowest — no instances, scales to zero | Medium — you size the instance | Low — managed, you pick node/PU capacity | Lowest — no instances, serverless |
| Data model | Document / key collections | Relational (Postgres, MySQL, SQL Server) | Relational, horizontally scalable | Columnar analytics / warehouse |
| Scaling | Automatic, per-operation | Vertical resize / read replicas | Horizontal, near-unlimited | Automatic, per-query |
| Consistency & reach | Strong, regional or multi-region | Single primary, regional HA | Strong, global, externally consistent | Analytic, not transactional |
| Reach for it when | App state with known document access | Standard relational OLTP at one-region scale | Relational that must scale globally with strong consistency | Analytics, reporting, and the data warehouse |

Decision procedure for a data store:

1. **Is the store for analytics, reporting, or a warehouse** rather than transactional app
   state? BigQuery. Stop here.
2. **Is the access document-shaped or key-based** with known query patterns and no ad-hoc
   joins? Firestore. Stop here.
3. **Does the workload need relational queries?** Then choose by scale:
   - One-region or regional-HA scale — Cloud SQL, sized to the load curve.
   - Global scale with strong consistency that outgrows a single primary — Spanner.
4. **Does a constraint rule out the managed engines** (a licensed database, an engine Google
   does not offer, an extension Cloud SQL forbids)? A self-managed database on Compute
   Engine — regional, automated backups, and a rehearsed restore, with the constraint
   recorded. Otherwise climb back to step 3.

Cache and messaging are managed too: Memorystore (Redis/Memcached) for an in-memory cache,
Pub/Sub for asynchronous decoupled delivery — never a Redis process hand-run on a VM where
Memorystore fits, and never a cron-on-a-box poller where a Pub/Sub push subscription
belongs.

## The serverless glue

A serverless-first architecture stitches its components together with managed integration
services, not with polling loops and cron on a VM:

- **Cloud Storage** — object storage, the default home for files, backups, static assets,
  and data-lake landing; durable and effectively infinite, no capacity to plan.
- **Pub/Sub** — a managed message bus to decouple producers from consumers and absorb
  bursts; a push subscription delivers the event without a polling loop.
- **Eventarc** — routes events from Google sources and Cloud Audit Logs to Cloud Run or
  Cloud Functions, replacing hand-wired event plumbing.
- **Workflows** — managed orchestration for a multi-step pipeline, replacing a hand-rolled
  state machine and its retry logic.
- **Identity Platform** — managed user identity, sign-up, and federation, replacing a
  hand-built auth service.
- **API Gateway** — a managed front door for Cloud Run or Cloud Functions, replacing a
  self-run reverse proxy.

## Failure modes

The recurring ways a team reaches past the serverless option and pays for it later:

- **Reflexive Compute Engine.** A VM fleet stood up because the team knows servers, where
  Cloud Run or Cloud Functions fits — now the team owns patching, scaling, and an on-call
  rotation Google would have carried.
- **Self-managed database.** Postgres on a VM "for control" — the control is mostly nightly
  backup scripts, failover that has never been tested, and version upgrades nobody
  schedules. Cloud SQL carries all three.
- **GKE where Cloud Run fits.** A full Kubernetes cluster stood up to run three stateless
  services, paying the cluster's operational tax for primitives the workload never uses.
- **Polling loop.** A cron job on a VM polling a bucket or a table every minute, where an
  Eventarc trigger or a Pub/Sub push would deliver the work and cost nothing while idle.
- **Hand-rolled auth.** A bespoke user store and password flow where Identity Platform
  carries sign-up, MFA, and federation as a managed service.
- **Always-on for a batch.** A 24x7 VM for a job that runs once a day, where a Cloud Run job
  or a scheduled Cloud Function billed per run would idle at zero.

## Red flags

A fast scan over a design — any one of the items below stops the line:

- A Compute Engine VM whose justification is habit, not a written constraint.
- A database engine hand-run on a VM where Cloud SQL, Firestore, or Spanner fits.
- A GKE cluster running only stateless containers that Cloud Run would carry.
- A polling loop or cron-on-a-box where an Eventarc or Pub/Sub trigger belongs.
- A self-built queue, scheduler, or auth service duplicating Pub/Sub, Workflows, or Identity
  Platform.
- An always-on resource serving a spiky or once-a-day workload.
- A "control" argument for a VM with no named capability the managed tier lacks.

## Worked example — a serverless-first reference architecture

A request-driven web API with a user store, an async processing path, and a relational
store, built so the team owns no VM at all. Every box is a managed service, and no
VM-forcing constraint ever appears, so none is provisioned.

```
              ┌──────────────────┐
  client ───▶ │ Identity Platform│  managed identity: sign-up, MFA, federation
              └────────┬─────────┘
                       │ authenticated request
              ┌────────▼─────────┐
              │   API Gateway    │  managed front door (HTTP, throttling, authz)
              └────────┬─────────┘
                       │ route
              ┌────────▼─────────┐        ┌──────────────┐
              │   Cloud Run      │ ─────▶ │  Firestore   │  serverless document, scales to zero
              │   (handler)      │        └──────────────┘
              └────────┬─────────┘
                       │ publish event (no polling)
              ┌────────▼─────────┐
              │     Pub/Sub      │  managed message bus, routes async work
              └────────┬─────────┘
                       │ push subscription
              ┌────────▼─────────┐        ┌──────────────────────┐
              │   Cloud Run      │ ─────▶ │  Cloud SQL (Postgres) │  relational, regional HA
              │   (worker)       │        └──────────────────────┘
              └────────┬─────────┘
                       │ archive
              ┌────────▼─────────┐
              │  Cloud Storage   │  durable object store + lifecycle to colder tiers
              └──────────────────┘
```

Why each rung was chosen, against the decision procedures above:

- **Compute** stops at Cloud Run for both the synchronous handler and the async worker: the
  work is a stateless container with no Kubernetes-specific need, and the bill drops to zero
  when idle. No host constraint appears, so the procedure never descends to GKE Autopilot or
  Compute Engine.
- **App data** is Firestore because the handler's access is document-shaped with known
  queries — the procedure stops at the document rung, no relational engine needed there.
- **Relational data** for the async path is Cloud SQL with regional HA: the path needs
  relational queries at one-region scale, below the threshold that would call for Spanner's
  global reach.
- **Integration** is Pub/Sub, not a polling loop — the handler publishes an event and a push
  subscription delivers it, so the worker costs nothing until there is work.
- **Identity** is Identity Platform and the **front door** is API Gateway — both managed, so
  no auth service and no reverse proxy are hand-run.
- **Archive** is Cloud Storage with a lifecycle rule tiering cold objects to Nearline, then
  Coldline, then Archive — durability and cost optimization with no storage capacity to
  plan.

Authoring this in Terraform (or Config Connector) and reading the plan before any apply is
the rest of the discipline: see the [IAM and SRE reference](iam-and-sre.md) for the
identity, encryption, network, and SLO posture each box still needs, and the
[Architecture Framework review](architecture-framework.md) for the five-category pass that
precedes provisioning. The apply against a live project is the approval-gated external mutation,
governed by the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
