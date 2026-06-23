# Operations — triage, dashboards, SOC2 evidence, and the response gate

The day-two discipline. A SOC is judged not on the rules it wrote but on what an analyst
does when one fires at 3 a.m. — and on whether the same telemetry that catches an intruder
also satisfies the auditor. The deterministic gates own config; this page owns the human
workflow, the dashboards that drive it, and the one rule that keeps an automated response
from becoming the incident.

## Severity tiers

Every alert carries a tier, and a tier with no response-time target and no owner is a wish,
not a process. A common four-tier scheme:

- **Critical** — active compromise or imminent loss (confirmed takeover, ransomware
  behavior, data exfiltration). Pages a human; minutes to acknowledge.
- **High** — strong indicator demanding same-shift attention (a brute-force success, a known
  exploit signature hitting a live service). A ticket and a near-term response target.
- **Medium** — worth review but not urgent (a single failed-login burst, a new listening
  port). A queue worked within the day.
- **Low / informational** — context and hunting fuel, dashboard-only, not a page.

Each tier names its response-time target and its owning role before the rule that feeds it
is enabled, so an alert always has somewhere to go and someone to go to.

## Triage workflow

The analyst's path from a raw alert to a defensible verdict. The same steps run for every
tier, scaled to its urgency:

1. **Acknowledge and scope.** Claim the alert so two analysts do not double-work it, and
   read the context it carries — the asset, the user, the source, the ATT&CK technique, the
   raw events behind the rule.
2. **Corroborate.** Pivot in Grafana from the single alert to the surrounding telemetry —
   the host's other events, the network flows to and from the source, the user's recent
   activity — to confirm or dissolve the signal. A lone alert with no corroboration is a
   different thing from one ringed by supporting evidence.
3. **Classify the verdict.** Decide among **true positive** (a real attack), **false
   positive** (the rule misfired — feed it back to [tuning](detection-engineering.md#tuning-and-false-positives)),
   and **benign-true-positive** (real behavior that is authorized — record the exception so
   it stops alerting).
4. **Contain or escalate on a true positive.** Match the response to the tier and the
   confidence: a low-blast-radius, reversible action under standing authority, or an
   escalation to incident response for anything broader. Any *blocking* action goes through
   the [approval gate](#active-response-the-approval-gate).
5. **Record the decision and close the loop.** Write the verdict, the evidence, and the
   action onto the alert so the trail is complete — for the next analyst, for the postmortem,
   and for the auditor.

A verdict with no recorded evidence is not triage; it is a guess that happens to close a
ticket.

## Dashboards — the single pane

Grafana drives the workflow, so the panels are built for the analyst's questions, not for
decoration:

1. **The live picture** — open alerts by severity and age, so the oldest critical surfaces
   first and nothing rots in the queue unseen.
2. **The triage queue** — unacknowledged alerts with their context inline, so an analyst
   starts work without leaving the panel.
3. **The ATT&CK matrix** — coverage and recent hits per technique, so a spike on one cell is
   visible against the map of what the SOC can and cannot see.
4. **Pipeline health** — agent connectivity, events-per-second, and sensor drop rate from
   Prometheus, so a collector that went silent is caught before its blind spot is exploited.
5. **The compliance view** — the SOC2 evidence panels (below), built to be screenshotted for
   an auditor, not reconstructed under deadline.

## SOC2 evidence

The monitoring is also the evidence trail. The same pipeline that detects an intruder
demonstrates the SOC2 Common Criteria around continuous monitoring and incident response —
each control names the stack component behind it and the artifact an auditor reads:

- **Continuous monitoring (CC7.1 / CC7.2)** — Wazuh and Suricata watching the estate without
  gaps — evidence: a coverage report showing every in-scope asset reporting, and the
  pipeline-health history proving it kept reporting.
- **Anomaly and intrusion detection (CC7.2)** — the tagged, tuned ruleset — evidence: the
  ATT&CK coverage matrix and a log of alerts raised, classified, and resolved.
- **Incident response (CC7.3 / CC7.4)** — the triage workflow and its records — evidence:
  triaged alerts carrying their verdict, evidence, timeline, and the action taken.
- **File integrity and change detection (CC6.8 / CC7.1)** — Wazuh FIM — evidence: a record
  of monitored-path changes with who and when.
- **Audit-log integrity (CC6.1)** — the immutable, retained event index — evidence: the
  retention configuration and the read-only access model showing the trail cannot be altered
  by the accounts it watches.

Evidence claimed with no component behind it, or a trail the watched accounts can rewrite,
fails the control regardless of how the dashboard looks.

## Active response — the approval gate

The one discipline that keeps the SOC from harming what it protects. Detection observes;
**active response mutates** — Wazuh `active-response` isolating a host or killing a process,
Suricata flipped from IDS to inline IPS, a firewall rule, a credential revocation. A mutation
fired on a false positive is a self-inflicted outage, so the gate holds:

1. **Detection-only is the default.** The system raises alerts; a human drives the response,
   unless a specific action has been pre-approved through the steps below.
2. **Every active-response path is pre-authorized in writing**, naming three things: the
   **trigger** (the exact, high-precision detection that may arm it), the **approver** (who
   signed off on letting it act, and whether it runs auto or human-in-the-loop), and the
   **rollback** (how the action is undone, rehearsed before it is armed).
3. **Auto-response is reserved for high-precision, low-blast-radius, reversible actions** —
   rate-limiting a source IP, killing a single known-malicious process — never a broad,
   destructive, or hard-to-reverse action on a guess.
4. **A standing kill switch disarms all auto-response** at once, so a misfiring rule that
   starts isolating healthy hosts is stopped in one move, not chased rule by rule.
5. **Flipping Suricata inline (IPS) is an infrastructure change**, governed by the
   [infra-safety discipline](../../../engineering/engineering/references/infra-safety.md):
   the change is planned, reviewed, and reversible before traffic rides through it, because
   an inline sensor that drops on a false positive is now a network outage.

An active-response path missing a trigger, an approver, or a rollback stays in alert-only
mode until it has all three.

## Failure modes

The recurring ways operations breaks:

- **The unread queue.** Alerts pile up faster than analysts work them, so the backlog hides
  the live incident and the SOC is blind while looking busy.
- **Verdict without evidence.** Tickets closed as "false positive" with no investigation, so
  a real attack is dismissed and the same noise returns untuned.
- **Auto-response without a kill switch.** An automated isolation rule on a false positive
  takes down healthy hosts, and nobody can stop it fast.
- **Evidence-by-deadline.** SOC2 artifacts reconstructed the week before the audit instead
  of produced continuously, so the evidence does not match what actually happened.
- **Inline-by-accident.** A sensor flipped to IPS without a rollback plan, so its first false
  positive is a production outage with no fast way back.
- **The silent collector.** An agent or sensor that stopped reporting, unnoticed because no
  panel watches pipeline health, leaving a blind spot the team believes is covered.

## Red flags

A fast scan over a running SOC — any one stops the line:

- A severity tier with no response-time target or no named owner.
- A closed alert carrying a verdict but no recorded evidence.
- An auto-response path with no kill switch.
- An active-response action with no named trigger, approver, or rollback.
- A SOC2 control claimed with no stack component behind it.
- No dashboard panel on agent connectivity or sensor drop rate.
- Suricata running inline (IPS) with no reviewed rollback plan.

## Worked example — triaging a suspicious process on a web VM

A High-tier alert fires: Wazuh flags a web VM executing an unexpected process — `curl`
piping a script to `bash` from the web-server user — mapping to ATT&CK **T1059** (Command
and Scripting Interpreter) with a hint of **T1105** (Ingress Tool Transfer).

1. **Acknowledge and scope.** The analyst claims the alert and reads its context: the asset
   (a public web VM), the user (the web-server service account, which should never spawn an
   interactive shell), the command line, and the parent process — the web server itself,
   suggesting a web exploit dropped the command.
2. **Corroborate.** Pivoting in Grafana from the one alert to the surrounding telemetry: the
   Suricata EVE log shows an inbound request to a known-vulnerable endpoint seconds earlier,
   an outbound flow to an unfamiliar IP fetching the script, and the Wazuh FIM log shows a
   new file written under `/tmp`. Three independent signals now ring the alert — this is not
   a lone misfire.
3. **Classify the verdict.** Web service account spawning a shell from a web request,
   fetching and writing a remote payload — **true positive**, an in-progress compromise, not
   an authorized admin action.
4. **Contain or escalate.** The blast radius is one VM and the action under consideration —
   isolating the host — is a *blocking* mutation, so it routes through the
   [approval gate](#active-response-the-approval-gate). Host isolation on a high-precision
   compromise indicator is a pre-authorized path here: its trigger is this exact
   correlation, its approver signed off on auto-isolation for confirmed payload-execution,
   and its rollback (re-attaching the VM's network) is rehearsed. The host is isolated; the
   standing kill switch remains available had the isolation begun hitting healthy hosts.
5. **Record and close the loop.** The analyst writes the verdict, attaches the corroborating
   evidence (the exploit request, the egress flow, the FIM write, the process tree), the
   timeline, and the isolation action onto the alert. That record is at once the incident
   postmortem's starting point and the SOC2 incident-response evidence (CC7.3 / CC7.4) — one
   artifact, two purposes.

Had the corroboration dissolved the signal (the "process" turning out to be an authorized
deploy script), the verdict would be benign-true-positive, the exception recorded, and the
rule fed back to [tuning](detection-engineering.md#tuning-and-false-positives) so it stops
alerting on that path — never silenced wholesale. The triage record, the evidence, and the
tuning feedback are grounded in the foundation doctrine's
[Genchi Genbutsu](../../../meta/foundation/SKILL.md) — the verdict rests on the real
telemetry the analyst pivoted through, never on the alert's say-so alone.
