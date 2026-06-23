# IAM and SRE — identity, the hierarchy, and reliability

The security and reliability floor of [the Architecture Framework](architecture-framework.md),
made concrete. Identity is the control plane of Google Cloud, and reliability is Google's
own SRE discipline of SLOs and error budgets — so this page carries both the lowest
tolerance for shortcuts and the measurable definition of "reliable enough". The
deterministic gates catch a malformed binding; this page catches the binding that parses
clean and still grants the whole project. Every workload clears this floor before it is
provisioned.

## The resource hierarchy — placement is a security decision

Google Cloud nests resources as **organization → folder → project → resource**. IAM policy
and org policy both inherit down this tree, so where a workload sits is a security decision,
not an accident of convenience.

Decision procedure:

1. **Organization** — the root, tied to a Cloud Identity or Workspace domain. An org-level
   binding reaches everything beneath, so reserve it for a small, audited break-glass group.
2. **Folders** — group projects by team, environment, or trust boundary. Bind policy at the
   folder so a new project inherits the right guardrails on creation.
3. **Projects** — the unit of billing, quota, and isolation. One workload per project keeps
   the blast radius small and cost attribution clean — the project is the isolation
   boundary.
4. **Org policy constraints** — guardrails the hierarchy enforces regardless of IAM. The
   high-value set: `storage.publicAccessPrevention`,
   `iam.disableServiceAccountKeyCreation`, `compute.requireOsLogin`, `sql.restrictPublicIp`,
   and domain-restricted sharing.

Org policy is a guardrail, not a suggestion: a constraint set at the folder blocks the
mistake even when a project owner tries to make it. Such a folder constraint is poka-yoke
applied to cloud governance.

Failure modes: one shared project for many workloads, so a mistake in one reaches the rest;
an org-level Owner binding on a human; no org policy, so any project can expose a bucket or
download a key; folders that mix production and development under one set of bindings.

Red flags: production and development sharing one project; `roles/owner` at the organization
or folder level on a person; no `storage.publicAccessPrevention` constraint; a project with
no folder and no inherited guardrail.

## IAM — least privilege

Decision procedure:

1. **Service accounts are workload identities, not shared logins.** Give each workload its
   own service account with a dedicated role binding, so a compromise is contained and an
   audit log attributes the action.
2. **Primitive roles are banned in practice.** `roles/owner`, `roles/editor`, and
   `roles/viewer` predate fine-grained IAM and grant sweeping access; Editor alone can alter
   most resources. Replace a primitive grant with a predefined role scoped to a service.
3. **Predefined roles first, custom roles second.** Reach for a Google-maintained predefined
   role (for example `roles/run.invoker`). When no predefined role fits, author a custom
   role listing only the permissions the task requires.
4. **Federate human access** through Cloud Identity or an external IdP with groups — no
   per-person Owner, no shared logins.
5. **Cap the break-glass path.** An organization or folder Owner binding lives on a
   monitored break-glass path with alerting on use, never as a standing grant.

Failure modes: a service account reused across unrelated workloads; `roles/editor` on an
automation account; a human with org-level Owner; a custom role that drifted into a
catch-all of permissions.

Red flags: `roles/owner` or `roles/editor` on a person or an automation account; a single
service account shared across services; a binding at the project level that belongs on one
resource.

## Workload Identity — no downloaded keys

A downloaded JSON service-account key is a long-lived secret that leaks and never expires on
its own. Workload Identity removes the key entirely.

Decision procedure:

1. **In-cluster on GKE** — GKE Workload Identity lets a Kubernetes service account
   impersonate a Google service account with short-lived, auto-rotated credentials. No key
   is mounted.
2. **Off-GCP (CI, another cloud, on-prem)** — Workload Identity Federation lets an external
   identity (a GitHub Actions runner, an AWS role, an OIDC token) impersonate a service
   account without a key.
3. **On Google compute** — Cloud Run, Cloud Functions, and Compute Engine attach a service
   account directly; the runtime fetches short-lived tokens from the metadata server.
4. **The genuinely-unavoidable key** — store it in Secret Manager, scope it tightly, and
   rotate it on a schedule. Set `iam.disableServiceAccountKeyCreation` so a key cannot be
   minted by default.

Failure modes: a JSON key checked into a repo or baked into an image; a CI pipeline holding
an exported key where Workload Identity Federation reaches; a key with no rotation and no
expiry; key creation left enabled org-wide.

Red flags: a downloaded service-account key anywhere in the stack; a key literal in code, a
variable file, or an image; `iam.disableServiceAccountKeyCreation` not enforced.

## Encryption — CMEK by default for sensitive data

Google encrypts data at rest by default with Google-managed keys. A regulated or
high-sensitivity workload upgrades to **customer-managed encryption keys (CMEK)** through
Cloud KMS, which puts key rotation, disabling, and destruction under your control.

Decision procedure:

1. Create a KMS key ring and a key per data domain, with automatic rotation set.
2. Point each CMEK-capable service (Cloud Storage, BigQuery, Cloud SQL, Compute disks,
   Pub/Sub) at the key through its `kms_key_name` setting.
3. Grant the service agent `roles/cloudkms.cryptoKeyEncrypterDecrypter` on that key, and
   nothing broader; separate the KMS admin role from the key-user role.
4. Treat scheduled key destruction as the most destructive act available — a destroyed key
   renders the ciphertext permanently unreadable, so route it through the approval gate.

Failure modes: sensitive data on default encryption where a compliance regime requires
CMEK; one key shared across every service; the KMS admin and key user held by the same
principal; rotation disabled.

Red flags: a data store with no CMEK key where compliance demands one; a single key across
all services; key destruction scheduled outside the approval gate.

## Network — closed by default

Decision procedure:

1. **Custom-mode VPC** — define subnets explicitly and size them to the workload, rather
   than an auto-mode VPC that opens a subnet in every region.
2. **Default-deny firewall** — deny ingress by default, then allow the exact ports and
   source ranges a service needs; a `0.0.0.0/0` allow on SSH (22), RDP (3389), or a database
   port is a finding.
3. **Private by default** — Cloud SQL, GKE nodes, and VMs take private IPs; outbound to
   Google APIs rides Private Google Access, not the public internet.
4. **VPC Service Controls** — draw a service perimeter around sensitive APIs (Cloud Storage,
   BigQuery) so data cannot be exfiltrated to a project outside the perimeter even with
   valid credentials.

Failure modes: an auto-mode VPC in production; a flat network with no segmentation; a
database with a public IP; egress wide open from a sensitive subnet.

Red flags: a firewall rule opening a management port to `0.0.0.0/0`; a Cloud SQL instance or
VM with a public IP; an auto-mode VPC in a production project; a sensitive API with no
service perimeter.

## SRE: SLOs and error budgets

Reliability on Google Cloud is measured the way Google measures it: a **service-level
objective (SLO)** sets the target, and the **error budget** is the room to fail underneath
it. An unreliable target nobody measures is a guess, not a reliability posture.

Decision procedure:

1. **Pick the SLI.** Choose a service-level indicator for the critical user journey —
   typically availability (the fraction of successful requests) or latency (the fraction
   served under a threshold). The SLI measures what the user actually experiences.
2. **Set the SLO.** State the target over a rolling window — for example 99.9% of requests
   succeed over 28 days. The SLO is a business decision about how reliable the journey must
   be, not the highest number reachable.
3. **Derive the error budget.** The budget is `1 − SLO` over the window: a 99.9% SLO permits
   roughly 43 minutes of failure per 30-day window. The budget is the currency reliability
   work and feature velocity both spend.
4. **Alert on the burn rate.** Wire a burn-rate alert in Cloud Monitoring that fires when
   the budget is being consumed fast enough to exhaust before the window closes — a fast
   burn pages now, a slow burn opens a ticket.
5. **Spend the budget as a policy.** A healthy budget buys feature velocity; an exhausted
   budget freezes risky releases until reliability is restored. The budget governs the
   release decision rather than a hunch.

Failure modes: a service with no SLO, so "reliable" is undefined and unarguable; an SLO set
at 100%, leaving no budget and no room to ship; a burn-rate alert nobody wired, so the
budget is spent silently; a release that proceeds while the budget is exhausted.

Red flags: a critical journey with no SLO; a 100% target; no burn-rate alert on the SLO; a
deploy policy that ignores a spent error budget.

## Logging, audit, and detection

An action nobody can reconstruct is an action nobody can defend in an audit. Observability
and audit are configured up front, not after the incident.

- **Cloud Logging** — centralize logs and route them through a log sink to a retention
  bucket, BigQuery, or Pub/Sub, with retention set to the compliance window.
- **Cloud Audit Logs** — Admin Activity logs are on by default; enable Data Access logs on
  sensitive services explicitly, since those record reads of data.
- **Security Command Center** — the org-wide posture and threat surface; the premium tier
  surfaces public buckets, open firewalls, and over-privileged accounts. Treat its findings
  as a work queue.
- **Log-based alerts** — alert on the high-signal events: a new Owner binding, a
  service-account key creation, an org-policy change, a firewall opened to the internet.

Red flags: Data Access logs off on a project holding regulated data; logs with no retention
or no sink; Security Command Center findings left unread.

## SOC2-relevant controls

This floor maps cleanly to the SOC2 Trust Services Criteria; each in-scope control names the
service behind it and the evidence an auditor reads:

- **Logical access (CC6)** — least-privilege IAM, no primitive roles, Workload Identity over
  keys, and the `iam.disableServiceAccountKeyCreation` org policy — evidence: scoped
  bindings, no downloaded keys, a reviewed access list.
- **Change management (CC8)** — Terraform in version control, a peer-reviewed plan, and the
  apply-approval gate — evidence: every infrastructure change traceable to a commit, a
  review, and an approval.
- **System monitoring (CC7)** — Cloud Audit Logs, Security Command Center, and log-based
  alerts — evidence: a trail of who changed what, when, and a detection path with an owner.
- **Confidentiality and encryption (C-series)** — CMEK through Cloud KMS, TLS in transit,
  and VPC Service Controls — evidence: every store on a declared key, no plaintext endpoint.
- **Availability (A-series)** — multi-zone design, an SLO with an error budget, and a tested
  restore — evidence: a measured reliability target and a rehearsed recovery path.

The evidence is the configuration itself: an auditor reads the Terraform, the org policies,
and the audit logs rather than a screenshot.

## The red-flag scan

A fast pass over a change — any one of the items below stops the line:

- A Cloud Storage bucket exposed to `allUsers` or `allAuthenticatedUsers`, or one without
  public-access prevention.
- `roles/owner` or `roles/editor` on a person or an automation account.
- A downloaded service-account key in code, a variable file, or an image.
- A data store with no CMEK key where compliance demands one.
- A firewall opening an admin port to `0.0.0.0/0`, or a data store with a public IP.
- A critical journey with no SLO and no error budget.
- Data Access logs off on a project holding regulated data.

## Worked example — the floor on a serverless-first stack

The [serverless-first reference architecture](managed-first.md#worked-example--a-serverless-first-reference-architecture)
(Identity Platform → API Gateway → Cloud Run → Firestore / Pub/Sub → Cloud Run worker →
Cloud SQL → Cloud Storage) clears the floor like this — and the serverless-first choices
shrink the attack surface, because there is no host to patch and no SSH port to expose:

- **Hierarchy** — the stack lives in its own project under the `prod` folder, separate from
  development, with org policy denying public buckets and denying service-account key
  creation inherited from the folder.
- **Identity** — each Cloud Run service runs as its own service account via Workload
  Identity; the handler's account holds only `datastore.user` on the one Firestore database
  and `pubsub.publisher` on the one topic, never a primitive role. No downloaded key exists
  anywhere in the stack. Human access comes through Cloud Identity groups.
- **Encryption** — Firestore, Cloud SQL, and Cloud Storage each declare a customer-managed
  KMS key with rotation on; API Gateway enforces TLS; the Cloud SQL credential lives in
  Secret Manager and is injected at runtime, never in the IaC.
- **Network** — the Cloud SQL instance has a private IP, reachable only over the VPC; Cloud
  Run reaches it through a Serverless VPC connector; a VPC Service Controls perimeter wraps
  Cloud Storage and BigQuery. No firewall opens an admin port, because there is no host to
  administer.
- **Reliability** — the critical journey carries a 99.9% availability SLO; the error budget
  is roughly 43 minutes per 30-day window; a burn-rate alert pages on a fast burn, and a
  spent budget freezes risky releases.
- **Audit** — a log sink writes to a retention bucket; Data Access logs are on for Firestore
  and Cloud SQL; Security Command Center is on; log-based alerts fire on a new Owner binding
  or a firewall opened to the internet.

A serverless-first design did not skip the floor — it made the floor smaller and cheaper to
hold, because every box Google runs is a box the team does not have to patch, key-rotate, or
firewall. The IAM bindings, KMS keys, org policies, and SLOs are authored as IaC and the
plan is read before any apply: the apply against a live project is the approval-gated
external mutation, governed by the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
