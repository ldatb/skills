# Security baseline — the non-negotiable floor

The security pillar of [Well-Architected](well-architected.md#2-security), made concrete.
Identity is the control plane of AWS, so this is the pillar with the lowest tolerance for
shortcuts. The deterministic gates catch a malformed policy; this page catches the policy
that parses clean and still grants the whole account. Every workload clears this floor
before it is provisioned.

## Multi-account and the landing zone

Decision procedure:

1. Separate environments and blast radii into their own AWS accounts under an
   **Organization** — production isolated from development at the account boundary, not
   merely the VPC boundary.
2. Stand up the foundation through a **landing zone** (AWS Control Tower or an equivalent
   Terraform baseline): a security account, a log-archive account, and guardrails applied
   org-wide.
3. Enforce coarse limits with **Service Control Policies** — deny regions out of scope,
   deny disabling CloudTrail, deny the root user's daily actions.

Failure modes: one account for everything, so a development mistake reaches production; no
SCP, so any account can turn off its own audit trail; a landing zone never stood up, so
each account re-derives its own (inconsistent) baseline.

Red flags: production and development sharing one account; CloudTrail that an account can
disable; no SCP guardrails on the Organization.

## IAM — least privilege

Decision procedure:

1. **Roles over keys.** Workloads assume IAM roles — instance profiles, task roles, IRSA,
   Lambda execution roles. Long-lived access keys are avoided; any that exist are
   inventoried and rotated.
2. **Scope every statement** to explicit actions and explicit resource ARNs.
3. **Reject wildcards.** `Action: "*"` and `Resource: "*"` are out, save a narrow,
   reviewed exception; prefer a managed job-function policy or a tightly scoped custom one.
4. **Cap with boundaries and conditions.** Permission boundaries limit delegated roles;
   conditions (source VPC, MFA present, tag match) narrow a grant further.
5. **Federate human access** through IAM Identity Center or an external IdP — no per-person
   IAM users with passwords, no shared logins.

Failure modes: a wildcard policy that turns one compromised credential into whole-account
access; access keys baked into an AMI or passed as environment variables; the root account
used in a pipeline; a role anyone can assume with no condition.

Red flags: `"Action": "*"` or `"Resource": "*"` in a policy; an access key in code, a
variable file, or an image; `AdministratorAccess` on a service role; the root user with an
active access key.

## Encryption by default

Decision procedure:

1. **At rest** — every data store (S3, EBS, RDS, DynamoDB, EFS) declares encryption with a
   KMS key, a customer-managed key (CMK) where the key policy and rotation must be controlled.
2. **In transit** — TLS on every endpoint; HTTP redirects to HTTPS; internal service calls
   ride TLS, not plaintext inside the VPC.
3. **Key management** — KMS key policies follow least privilege, automatic rotation is on,
   and key administrators are separated from key users.
4. **Secrets** — credentials live in Secrets Manager or SSM Parameter Store
   (SecureString), injected at runtime; never in code, an AMI, a container layer, or a plan
   output.

Failure modes: an unencrypted EBS volume or RDS instance; an S3 bucket with no default
encryption; a load balancer terminating only on port 80; a database password in a committed
Terraform variable file.

Red flags: a data store with no KMS key declared; a plaintext (port 80 only) endpoint; a
secret literal in the diff; key rotation disabled.

## Network — closed by default

Decision procedure:

1. **VPC layout** — public subnets for ingress only (load balancers, NAT); private subnets
   for compute and data.
2. **Private by default** — instances, containers, and databases sit in private subnets
   with no public IP; outbound rides a NAT gateway or a VPC endpoint.
3. **Scoped security groups** — open the exact port to the exact source; reference another
   security group rather than a CIDR range where the call is internal; never `0.0.0.0/0` to
   a workload or admin port.
4. **VPC endpoints** — Gateway endpoints for S3 and DynamoDB, Interface endpoints for other
   services, to keep traffic off the public internet.

Failure modes: a database with a public IP; a flat single subnet for everything; an admin
port open to the internet; cross-environment traffic on a shared security group.

Red flags: a security group opening port 22 or 3389 to `0.0.0.0/0`; a database reachable
from the internet; a single subnet holding both ingress and data tiers.

## Audit and detection

Decision procedure:

1. **CloudTrail** — a multi-region, organization-wide trail captures management events (and
   data events where needed) to a locked-down bucket in the log-archive account, with
   log-file validation on.
2. **AWS Config** — records resource configuration and evaluates conformance rules
   (encryption present, public access blocked, required tags) continuously.
3. **GuardDuty** — threat detection enabled across all accounts and regions, findings
   routed to a responder or SIEM.
4. **CloudWatch** — platform and application logs centralized, with metric filters and
   alarms on the signals that matter.

Failure modes: CloudTrail off or single-region; the trail bucket writable by the accounts
it audits; GuardDuty findings with no destination; logs with no retention policy.

Red flags: CloudTrail disabled or single-region; a trail bucket the workload accounts can
write; GuardDuty off in any active region; an audit log with no retention.

## SOC2-relevant controls

The baseline maps cleanly to the SOC2 Trust Services Criteria; each in-scope control names
the service behind it and the evidence an auditor reads:

- **Audit logging** — CloudTrail + Config + CloudWatch — evidence: an immutable, retained
  trail of who changed what, when.
- **Access control** — IAM least privilege + Identity Center + MFA — evidence: scoped
  policies, no shared accounts, a reviewed access list.
- **Encryption** — KMS at rest + TLS in transit — evidence: a Config rule showing every
  store encrypted, no plaintext endpoints.
- **Change management** — IaC in version control + a reviewed plan + a pipeline — evidence:
  every infrastructure change traceable to a commit, a review, and an approval.
- **Availability and monitoring** — multi-AZ + backups + alarms — evidence: tested restores
  and an alerting path with an owner.

Red flags: a control claimed with no service behind it; change management asserted while
console edits bypass the pipeline; an access list nobody has reviewed.

## The red-flag scan

A fast pass over any change — any one stops the line:

- An S3 bucket without `block_public_access` and default encryption.
- An IAM statement with `"*"` in `Action` or `Resource`.
- A credential or key literal in code, a variable file, or an image.
- CloudTrail disabled, single-region, or writing to an unprotected bucket.
- A security group opening an admin port to `0.0.0.0/0`.
- A data store with no KMS key.
- Production and development sharing one account with no SCP guardrail.

## Worked example — the baseline on a managed-first stack

The [managed-first reference architecture](managed-first.md#worked-example--a-managed-first-reference-architecture)
(Cognito → API Gateway → Lambda → DynamoDB / EventBridge → Aurora Serverless v2 → S3) clears
the floor like this — and the managed-first choices shrink the attack surface, because there
is no host to patch and no SSH port to expose:

- **Accounts** — the stack lives in a workload account under the Organization, separate from
  development, with SCP guardrails denying out-of-scope regions and denying anyone the power
  to disable CloudTrail.
- **Identity** — each Lambda assumes its own least-privilege execution role; the handler's
  role grants only `dynamodb:PutItem` and `dynamodb:GetItem` on the one table ARN and
  `events:PutEvents` on the one bus, never a wildcard. No access key exists anywhere in the
  stack. Human access comes through IAM Identity Center.
- **Encryption** — DynamoDB, Aurora Serverless v2, and S3 each declare a customer-managed
  KMS key with rotation on; API Gateway enforces TLS; the Aurora credential lives in Secrets
  Manager and is injected at runtime, never in the IaC.
- **Network** — the Aurora cluster sits in private subnets with no public IP, reachable only
  from the worker Lambda's security group; S3 and DynamoDB are reached through Gateway VPC
  endpoints, off the public internet. No security group opens an admin port, because there
  is no host to administer.
- **Audit** — a multi-region CloudTrail writes to the log-archive account; Config rules
  assert encryption-present and public-access-blocked on every store; GuardDuty is on across
  regions; CloudWatch alarms fire on Lambda errors and API Gateway 5xx.

A managed-first design did not skip the baseline — it made the baseline smaller and cheaper
to hold, because every box AWS runs is a box the team does not have to patch, key-rotate, or
firewall. The IAM policies, KMS keys, and Config rules are authored as IaC and the plan is
read before any apply: the apply is the approval-gated external mutation, governed by the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — read the real plan, never assume it.
