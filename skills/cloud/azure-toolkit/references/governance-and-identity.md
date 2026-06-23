# Governance and identity — the non-negotiable floor

Identity is the new perimeter on Azure, and governance is how that perimeter scales past one
subscription. This page is the security pillar of [Well-Architected](well-architected.md#2-security)
made concrete, framed by the Cloud Adoption Framework. The deterministic gates catch a
malformed role assignment; this page catches the assignment that parses clean and still
grants the whole subscription. Every workload clears this floor before it is provisioned.

## Landing zones — the Cloud Adoption Framework hierarchy

The Cloud Adoption Framework organizes a tenant top-down so a new subscription *inherits*
its controls rather than re-deriving them. The hierarchy is **management group → subscription
→ resource group → resource**.

Decision procedure:

1. Build the **management-group hierarchy** under the tenant root: a platform group (for
   identity, management, and connectivity subscriptions) and a landing-zones group (for
   workload subscriptions), so policy and RBAC assigned at a group flow down to every
   subscription beneath it.
2. Separate environments and blast radii into their own **subscriptions** — production
   isolated from development at the subscription boundary, not merely the VNet boundary.
3. Stand up the platform foundation as **landing zones** (the Azure landing zone accelerator
   or an equivalent Bicep/Terraform baseline): a management subscription for Log Analytics and
   automation, an identity subscription, and a connectivity subscription for the hub network.
4. Enforce coarse limits with **Azure Policy at the management group**: deny out-of-scope
   regions, deny public network access on data services, deny resource types out of scope.

Failure modes: one subscription for everything, so a development mistake reaches production;
no management-group policy, so each subscription re-derives its own inconsistent baseline; a
landing zone never stood up, so governance is bolted on per workload after the fact.

Red flags: production and development sharing one subscription; no Azure Policy assigned at
the management-group scope; a flat tenant with every workload in the root subscription.

## Entra ID, managed identities, and RBAC — least privilege

The control plane and most data planes authenticate through Microsoft Entra ID, so the
identity model is the security model.

Decision procedure:

1. **Managed identities over secrets.** A compute resource (App Service, Functions, Container
   Apps, AKS, VM) authenticates to other Azure services through a system- or user-assigned
   managed identity. No connection string, no client secret, no key in app settings.
2. **Scope every RBAC assignment** to the narrowest built-in role at the narrowest scope —
   resource first, then resource group, then subscription. Prefer `Contributor` on one
   resource group, or a purpose-built custom role, over `Owner` higher up.
3. **Reject broad grants.** `Owner` at subscription or management-group scope on a service
   principal is out, save a narrow, reviewed exception; `Owner` on a human is replaced by
   just-in-time elevation.
4. **No standing privilege where avoidable.** Human admin access goes through Privileged
   Identity Management with just-in-time elevation and approval, not a permanent assignment.
5. **Federate pipeline access.** CI authenticates with OIDC workload-identity federation,
   removing the long-lived service-principal secret from the pipeline.

Failure modes: a broad `Owner` grant that turns one compromised principal into
whole-subscription access; a client secret baked into an image or passed as an app setting; a
permanent admin role where just-in-time elevation belongs; a long-lived service-principal
secret in CI.

Red flags: `Owner` at subscription or management-group scope on a non-human principal; a
client secret, connection string, or key in code, a config file, or app settings;
`AdministratorAccess`-equivalent breadth on a service identity; a permanent privileged
assignment on a human.

## Encryption — Key Vault, at rest, in transit

Decision procedure:

1. **Key Vault as the secret boundary.** Keys, secrets, and certificates live in Azure Key
   Vault with RBAC authorization, soft-delete, and purge protection on. Applications read them
   at runtime through a managed identity; secrets never land in source, image layers, or logs.
2. **At rest.** Platform encryption is on by default; regulated data adds a customer-managed
   key (CMK) backed by Key Vault, with infrastructure (double) encryption where the data class
   demands it.
3. **In transit.** TLS 1.2 or higher on every endpoint; HTTPS-only on storage and web tiers;
   plaintext protocols disabled.
4. **Key management.** Key Vault access follows least privilege through RBAC, key rotation is
   on, and key administrators are separated from key users.

Failure modes: an unencrypted regulated data store; a storage account with shared-key access
left enabled; a web tier terminating only on plaintext; a database credential in a committed
variable file.

Red flags: a regulated data store with no CMK declared; a plaintext-only endpoint; a secret
literal in the diff; key rotation disabled; shared-key access enabled on a storage account.

## Network — closed by default

Decision procedure:

1. **Private by default.** PaaS data services (Storage, Azure SQL, Cosmos DB, Key Vault)
   expose a private endpoint inside the VNet and disable public network access. A storage
   account reachable from the internet is the most common Azure breach vector.
2. **Segmentation with NSGs.** Network Security Groups gate subnet traffic with explicit
   allow rules and a default deny; an NSG rule opening `0.0.0.0/0` to port 22 or 3389 is a
   blocker.
3. **Egress control.** Outbound traffic routes through Azure Firewall or a NAT gateway, and a
   public web workload sits behind Application Gateway with WAF, or Front Door.
4. **Private DNS.** Private DNS zones resolve private-endpoint records inside the VNet so
   clients reach the private IP rather than the public name.

Failure modes: a database with public network access enabled; a flat single subnet for
everything; an admin port open to the internet; cross-environment traffic on a shared subnet.

Red flags: an NSG opening port 22 or 3389 to `0.0.0.0/0`; a data service reachable from the
internet; a single subnet holding both ingress and data tiers.

## Governance — Azure Policy, Defender, Monitor

Decision procedure:

1. **Azure Policy** codifies guardrails as assignments: deny public storage, require tags,
   restrict regions, enforce CMK. Policy is the structural control that makes the
   misconfiguration impossible rather than merely discouraged (poka-yoke).
2. **Defender for Cloud** enables the Defender plans for the resource types in use; the team
   tracks the Secure Score and triages high-severity recommendations.
3. **Azure Monitor and Log Analytics** route diagnostic settings on every resource to a Log
   Analytics workspace, set activity-log alerts on privileged operations, and retain logs to
   the period the compliance regime requires.

Failure modes: guardrails written as a wiki page instead of a policy assignment; Defender off
on an in-use resource type; diagnostic settings unset, so an incident has no audit trail.

Red flags: a guardrail with no policy assignment behind it; Defender for Cloud off; a resource
with no diagnostic settings and no Log Analytics destination.

## SOC2-relevant controls

The baseline maps cleanly to the SOC2 Trust Services Criteria; each in-scope control names the
service behind it and the evidence an auditor reads:

- **Security / access (CC6).** Entra ID with MFA + RBAC least privilege + PIM just-in-time +
  Key Vault + private networking — evidence: scoped role assignments, no shared accounts, a
  reviewed access list.
- **Change management (CC8).** IaC in version control + a reviewed plan + a pipeline —
  evidence: every infrastructure change traceable to a commit, a review, and an approval.
- **Monitoring (CC7).** Defender for Cloud + Log Analytics + activity-log alerting — evidence:
  an immutable, retained trail of who changed what, when.
- **Availability (A1).** Zone-redundant deployment + geo-redundant backup + tested recovery
  objectives — evidence: a tested restore and an alerting path with an owner.

The auditor wants evidence: the policy assignment, the diagnostic setting, the access review,
the plan in the pipeline log. A control with no evidence trail is a control with a gap.

## Red flags

A fast pass over any change — any one of these stops the line:

- An `Owner` role assignment at subscription or management-group scope on a non-human
  principal.
- A storage account, SQL server, Cosmos account, or Key Vault with public network access
  enabled.
- A client secret, connection string, or key in source, a config file, or app settings.
- An NSG rule allowing `0.0.0.0/0` inbound to port 22 or 3389.
- A resource with no diagnostic settings and no Log Analytics destination.
- A plan that shows an unexplained `replace` on a database, disk, or volume.
- A deploy or portal change proposed without a captured, human-read plan.
- Production and development sharing one subscription with no management-group policy.

## Worked example — the baseline on a PaaS-first stack

The [PaaS-first reference architecture](managed-first.md#worked-example--a-paas-first-reference-architecture)
(Front Door → App Service → Azure SQL Database, with Service Bus → Functions → Blob Storage)
clears the floor like this — and the PaaS-first choices shrink the attack surface, because
there is no host to patch and no SSH port to expose:

- **Hierarchy** — the stack lives in a workload subscription under the landing-zones
  management group, separate from development, with Azure Policy assigned at the group denying
  out-of-scope regions and denying public network access on data services.
- **Identity** — App Service and the Functions app each carry a system-assigned managed
  identity; the web app's identity holds `db_datareader` and `db_datawriter` on the one Azure
  SQL database and Storage Blob Data Contributor on the one container, never `Owner`. No
  connection string exists anywhere in the stack. Human access comes through Entra ID with PIM.
- **Encryption** — Azure SQL, Blob Storage, and Service Bus each declare a customer-managed
  key in Key Vault with rotation on; Front Door and App Service enforce TLS; the Key Vault has
  soft-delete and purge protection on, and the app reads secrets through its managed identity.
- **Network** — Azure SQL, the storage account, and Service Bus expose private endpoints with
  public network access disabled, reachable only from the App Service and Functions VNet
  integration; no NSG opens an admin port, because there is no host to administer.
- **Governance** — Defender for Cloud is on for App Service, SQL, and Storage; diagnostic
  settings on every resource route to the platform Log Analytics workspace; an activity-log
  alert fires on privileged role assignments; Azure Monitor alerts on App Service 5xx.

A PaaS-first design did not skip the baseline — it made the baseline smaller and cheaper to
hold, because every box Azure runs is a box the team does not have to patch, key-rotate, or
firewall. The RBAC assignments, Key Vault keys, and Policy assignments are authored as IaC and
the plan is read before any deploy: the deploy is the approval-gated external mutation,
governed by the [infra-safety discipline](../../../engineering/engineering/references/infra-safety.md)
and grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
