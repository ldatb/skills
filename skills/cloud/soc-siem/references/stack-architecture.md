# Stack architecture — Wazuh + Suricata + Grafana for cloud and VMs

The topology a SOC engineer lays before writing a single rule. The question on every host
and every segment is not "can I see it?" but "where does its telemetry enter the pipeline,
and is the collector scoped so a compromise of the collector is not a compromise of the
estate?" The deterministic gates own config syntax; this page owns the placement they
cannot encode.

## The three roles

- **Wazuh** — host-based detection. An agent on each VM and container ships logs, runs file
  integrity monitoring (FIM), reports installed packages for vulnerability detection, and
  enforces security-configuration checks. Agents report to the **Wazuh manager** (decoding,
  rules, alerting); the manager indexes events into the **Wazuh indexer** (an OpenSearch
  fork) for search and retention. Agentless collectors pull cloud logs (CloudTrail, S3
  access, GuardDuty) where no host exists to carry an agent.
- **Suricata** — network detection. A sensor inspects traffic on a SPAN/mirror port, a TAP,
  or a cloud traffic-mirroring session, matching signatures and decoding protocols, and
  emits **EVE JSON** (alerts, flows, DNS, TLS, HTTP metadata). In IDS mode it observes; in
  IPS mode it sits inline and can drop — the inline mode is the approval-gated posture, not
  the default.
- **Grafana** — visualization. Dashboards query the Wazuh indexer for security events, Loki
  for raw log search, and Prometheus for the health metrics of the stack itself. Grafana is
  the SOC's single pane: the live alert picture, the triage queues, and the compliance
  evidence all render here.

Loki carries logs that are not security alerts but are needed for context and search;
Prometheus carries the metrics that prove the pipeline itself is alive (agent connectivity,
events-per-second, sensor drop rate). A blind monitoring stack is worse than none, so the
stack monitors itself.

## Topology decision procedure

1. **Place the manager and indexer centrally**, reachable from every network the agents
   live in, sized for the peak events-per-second of the estate. In a multi-account cloud,
   the manager and indexer sit in a dedicated security account, isolated from the workloads
   they watch.
2. **Deploy a Wazuh agent on every in-scope VM and container image** — bake the agent into
   the golden image so a new host enrolls on boot, rather than being patched in by hand
   afterward. A host that cannot carry an agent (a managed database, a serverless function)
   routes its logs through an agentless or cloud-native collector instead.
3. **Place a Suricata sensor on each segment whose traffic can be mirrored or tapped** — a
   VPC traffic-mirror target in the cloud, a SPAN port on-prem. A segment whose traffic
   cannot be captured records that gap explicitly, so the blind spot is known, not assumed.
4. **Connect every cloud log source** the threat model needs — CloudTrail for the API
   control plane, VPC flow logs for network metadata, the load-balancer and WAF logs for
   the edge — into the pipeline through a least-privilege pull role.
5. **Stand up Grafana with read-only data sources** pointed at the indexer, Loki, and
   Prometheus, and a separate alerting path for the signals that page.

## Least-privilege for collectors

Every collector is a credential an attacker would love, so each is scoped to read exactly
what it ships and nothing more:

1. **Cloud log pull** uses a read-only role — `s3:GetObject` on the one CloudTrail bucket
   prefix, `logs:FilterLogEvents` on the named groups — never an account-wide reader and
   never a write or delete permission.
2. **The agent's local identity** runs with the least OS privilege that still reads the log
   paths and computes FIM hashes; the agent does not need, and does not get, broad root
   capability beyond that.
3. **The indexer and Grafana** authenticate over TLS with scoped service accounts; Grafana's
   data-source credential is read-only, so a Grafana compromise cannot rewrite the evidence.
4. **The Suricata sensor** sees a copy of traffic on a one-way mirror — the capture path
   carries no ability to inject, so a sensor compromise cannot reach back into the network.

## The pipeline

The spine of the whole system is six stages — **collect → normalize → detect → alert →
triage → respond** — and every later page hangs off it:

1. **Collect** — agents, sensors, and cloud pullers gather raw telemetry: host logs, FIM
   events, package inventories, EVE JSON, CloudTrail records.
2. **Normalize** — Wazuh decoders parse raw lines into a consistent field set (source IP,
   user, process, action) so a rule written once matches across log formats. Unparsed
   telemetry cannot be reasoned about, so a decoder gap is a detection gap.
3. **Detect** — the normalized event is scored against the ruleset (Wazuh rules, Suricata
   signatures, Sigma compiled to the backend), producing an alert with a level and, where
   tagged, a MITRE ATT&CK technique.
4. **Alert** — an alert above the routing threshold reaches a channel with an owner (a
   ticket queue, a pager, a Grafana panel), carrying the context an analyst needs to start.
5. **Triage** — an analyst works the alert from raw signal to a verdict (true positive,
   false positive, benign-true-positive), per the [operations triage workflow](operations.md#triage-workflow).
6. **Respond** — a confirmed incident drives a response; any *blocking* response is
   approval-gated, per the [operations response-gating section](operations.md#active-response-the-approval-gate).

## Failure modes

The recurring ways a topology leaks or goes blind:

- **Coverage gaps.** A subnet with no sensor and no mirror, or a host class with no agent,
  so an attacker who lands there is invisible — the gap was never recorded, so nobody knew.
- **Over-privileged collector.** A cloud-log role with `s3:*` or an account-wide reader,
  turning one stolen collector credential into estate-wide access.
- **Single point of failure.** One manager with no standby, so a manager outage blinds the
  whole SOC and the gap goes unnoticed because nothing watches the watcher.
- **Unmonitored pipeline.** No Prometheus on agent connectivity or sensor drop rate, so an
  agent that stopped reporting a week ago looks identical to a host with nothing to report.
- **Indexer as a swamp.** Everything retained forever with no tiering, so storage cost
  balloons and queries crawl, and the retention needed for evidence is lost in the noise.
- **Mutable evidence.** Grafana or an analyst account with write access to the indexed
  events, so the audit trail an attacker (or an auditor) reads can be altered.

## Red flags

A fast scan over a topology — any one stops the line:

- An in-scope network segment with no sensor and no recorded reason for the gap.
- A host class in scope with no Wazuh agent and no agentless collector.
- A cloud-log collector role carrying a wildcard, a write, or a delete permission.
- A single Wazuh manager with no standby for a production SOC.
- No metric on agent connectivity or sensor drop rate — the pipeline does not watch itself.
- A Grafana or analyst credential that can write to the event index.

## Worked example — monitoring a hybrid cloud-and-VM estate

A web platform across one AWS account and a fleet of Linux VMs, with a managed database and
a public edge, instrumented so every tier reports and no collector is over-trusted:

```
  ┌──────────────────────────────────────── AWS workload account ─────────────────────────┐
  │                                                                                         │
  │  ALB / WAF ──┐         EC2 web VMs ──┐         RDS (managed) ──┐                         │
  │  (edge logs) │         (Wazuh agent) │         (no agent)      │                         │
  │              │                       │                         │                         │
  │  VPC flow ───┤   traffic mirror ─▶ Suricata sensor             │ CloudWatch / RDS logs   │
  │  CloudTrail ─┤      (EVE JSON)        │                         │                         │
  └──────────────┼───────────────────────┼─────────────────────────┼─────────────────────────┘
                 │                        │                         │
   read-only pull│         agent shipping │            agentless pull│   (all least-privilege)
                 ▼                        ▼                         ▼
        ┌───────────────────────── security account ──────────────────────────┐
        │  Wazuh manager (decode + rules) ─▶ Wazuh indexer (search/retention)  │
        │  Loki (raw logs)   Prometheus (stack health)                         │
        └───────────────────────────────┬─────────────────────────────────────┘
                                         │ read-only data sources
                                         ▼
                                   ┌───────────┐
                                   │  Grafana  │  single pane: alerts, triage, SOC2 evidence
                                   └───────────┘
```

Why each placement was chosen, against the procedures above:

- **Host telemetry** — each EC2 web VM carries a Wazuh agent baked into the golden AMI, so a
  scaled-up instance enrolls on boot; the agent ships auth logs, FIM on the web root, and a
  package inventory for vulnerability detection.
- **The managed database** carries no agent (no host to install on), so its audit and error
  logs flow through an agentless CloudWatch pull on a role scoped to those log groups alone.
- **Network telemetry** — a VPC traffic-mirror session copies the web tier's traffic to a
  Suricata sensor running IDS-only; the sensor emits EVE JSON and cannot inject, because the
  mirror is one-way. Flipping it to inline IPS is a separate, approval-gated change.
- **Cloud control plane** — CloudTrail and VPC flow logs feed the manager through a
  read-only pull role granting `s3:GetObject` on the trail prefix and nothing else; no
  collector holds a write or delete.
- **The brain** sits in a dedicated security account, isolated from the workload account, so
  a workload compromise does not reach the manager, the indexer, or the evidence.
- **The single pane** is Grafana with read-only data sources over the indexer, Loki, and
  Prometheus — the analysts read the evidence, and no analyst account can rewrite it.

The configs (agent profiles, Suricata rules, decoders, dashboards) are authored as code and
reviewed before rollout, and the one mutation that matters — flipping a sensor inline or
arming an active response — is held behind approval, per the
[infra-safety discipline](../../../engineering/engineering/references/infra-safety.md) and
grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — verify the live pipeline by injecting
a test event, never assume it flows.
