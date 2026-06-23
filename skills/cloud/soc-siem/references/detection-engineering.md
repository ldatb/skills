# Detection engineering — rules, ATT&CK mapping, and tuning

Where a SOC earns its keep. A stack that collects everything and detects nothing is a log
archive, not a SIEM. The craft is writing detections that fire on the adversary behavior in
the threat model, tagging each so coverage is measurable, and tuning each so its alerts are
worth an analyst's attention. The deterministic gates own rule syntax; this page owns
whether the rule detects the right thing without drowning the queue.

## Anatomy of a detection

A detection has three parts, and a gap in any one makes it untrustworthy:

- **The logic** — a Wazuh rule (matching decoded fields, with a level), a Suricata signature
  (matching packet or protocol content), or a **Sigma** rule compiled to the backend so one
  portable definition targets multiple engines.
- **The mapping** — a **MITRE ATT&CK** technique id (e.g. `T1110` Brute Force) so the
  detection's place in the kill chain is explicit and coverage gaps are visible on a matrix.
- **The test** — a malicious sample the rule must fire on, and a benign sample it must stay
  silent on. A rule with no test is a guess; a rule that fires on the benign sample is noise.

## Writing a detection — the decision procedure

1. **Name the behavior, not the tool.** Start from an ATT&CK technique or a threat-model
   entry ("an attacker brute-forces SSH"), so the detection survives a change of attacker
   tooling. A detection keyed to one tool's name dies the day the attacker renames the tool.
2. **Pick the layer that sees it.** Host-visible behavior (failed logins, a new SUID binary,
   a modified config) goes to a Wazuh rule; wire-visible behavior (a C2 beacon, an exploit
   payload, a DNS-tunnel pattern) goes to a Suricata signature. A behavior visible at both
   layers gets a detection at each, and the two corroborate.
3. **Prefer correlation over a single line.** A single failed login is noise; *N* failures
   then a success from one source is an account takeover. Wazuh's frequency and
   `if_matched_sid` correlation expresses the sequence the raw event cannot.
4. **Write the logic against normalized fields**, not raw text, so the rule matches across
   log formats — a brute-force rule keyed to the normalized `srcip` and `dstuser` fields
   works for SSHD, for a web login, and for a cloud sign-in API alike.
5. **Tag the ATT&CK technique** in the rule so coverage rolls up onto the matrix and the
   gaps are visible. An untagged detection cannot be counted toward coverage.
6. **Ship the test pair** — the fire-on-malicious and silent-on-benign samples — and run
   them in the rule-test harness before merge.

## ATT&CK mapping — making coverage visible

The ATT&CK matrix is the coverage map, and the goal is to know the gaps, not to fill every
cell:

1. **Tag every detection** with its technique id (and sub-technique where it applies), so
   each shipped rule lands on a cell of the matrix.
2. **Render the matrix in Grafana** — cells with a tagged, enabled detection are covered;
   empty cells in the threat model are gaps.
3. **Prioritize gaps by the threat model**, not by the matrix's size — a technique the named
   adversary actually uses outranks an exotic one nobody in scope faces. Chasing full-matrix
   coverage is how a SOC burns months detecting techniques irrelevant to its estate.
4. **Track coverage as a metric over time**, so a regression (a disabled rule reopening a
   cell) surfaces rather than rotting silently.

## Tuning and false positives

The core risk of the whole program. An alert stream an analyst stops trusting is worse than
no alerts, because it trains the team to ignore the one that mattered. Every enabled rule
clears a precision bar before it pages anyone:

1. **Baseline against normal.** Run the rule in alert-only mode over a window of
   representative traffic and count its hits. A rule firing hundreds of times a day on
   normal activity is not a detection yet.
2. **Classify the hits.** Sort the baseline alerts into true positive, false positive, and
   benign-true-positive (real behavior that is authorized — a vulnerability scanner, a
   backup job, an admin's bulk action).
3. **Cut the false positives at the source** in this order: scope the rule (exclude the
   known-benign source, user, or asset by identity, not by muting the whole rule);
   threshold it (require *N* occurrences, or a rate, before it fires); enrich it (require a
   second corroborating signal). Disabling the rule is the last resort, recorded with the
   reason.
4. **Measure precision** — true positives over all alerts — over the baseline window, and
   compare it to the bar the program set per severity (a paging rule needs higher precision
   than a dashboard-only one). A rule that cannot clear its bar after scoping and
   thresholding ships disabled, not merged, so the queue stays trustworthy.
5. **Re-baseline on drift.** Re-run the baseline when the environment changes (a new app, a
   new traffic pattern), so a rule that was precise last quarter does not quietly become
   noise this one.

## Failure modes

The recurring ways detection engineering goes wrong:

- **Alert fatigue.** A flood of low-value alerts trains the analysts to dismiss the queue,
  so the true positive arrives and is closed unread with everything else.
- **Tool-keyed brittleness.** A rule matching a specific tool's user-agent or filename,
  defeated the moment the attacker changes one string, while the underlying behavior sails
  through.
- **Coverage theater.** A green ATT&CK matrix built from rules that have never fired on a
  real sample — coverage claimed, detection absent.
- **Mute-the-rule tuning.** A noisy rule silenced wholesale instead of scoped, so the
  authorized scanner stops alerting and so does the real attacker using the same technique.
- **Untested detection.** A rule shipped with no fire-and-silence pair, so nobody knows
  whether it catches the threat or only the demo.
- **Threshold set blind.** A frequency threshold picked from a guess, not a baseline, set so
  high the attack stays under it or so low the noise sails over it.

## Red flags

A fast scan over a ruleset — any one stops the line:

- An enabled paging rule with no recorded precision over a baseline window.
- A detection with no MITRE ATT&CK technique tag.
- A rule matching a literal tool name, filename, or user-agent rather than a behavior.
- A rule disabled to silence noise, with no scoping attempt and no recorded reason.
- A merged detection with no fire-on-malicious / silent-on-benign test pair.
- An ATT&CK matrix counting rules that have never fired on a real sample.

## Worked example — detecting SSH brute force, mapped and tuned

A threat-model entry: *an attacker brute-forces SSH on an internet-reachable VM* — ATT&CK
**T1110** (Brute Force), escalating to **T1078** (Valid Accounts) on a successful login.

**The logic.** Host-visible (failed logins land in the VM's auth log and the Wazuh agent
ships them), so the detection is a Wazuh correlation rule, not a single-event match. The
base SSHD decoder normalizes each failure to `srcip` and `dstuser`; the correlation rule
fires when one `srcip` accumulates *N* failures inside a time window, and a higher-severity
rule fires when a failure burst from that `srcip` is followed by a `success` for the same
user — the brute-force-then-takeover sequence:

```
# Wazuh-style correlation (illustrative)
<rule id="100200" level="10" frequency="8" timeframe="120">
  <if_matched_sid>5716</if_matched_sid>   <!-- 5716 = sshd failed password -->
  <same_source_ip />
  <description>SSH brute force: 8+ failures from one source in 120s</description>
  <mitre><id>T1110</id></mitre>
</rule>

<rule id="100201" level="12" frequency="1" timeframe="300">
  <if_matched_sid>100200</if_matched_sid>  <!-- a brute-force burst already fired -->
  <if_sid>5715</if_sid>                     <!-- 5715 = sshd authentication success -->
  <same_source_ip />
  <description>SSH login succeeded from a source that just brute-forced — likely takeover</description>
  <mitre><id>T1078</id></mitre>
</rule>
```

**The mapping.** Rule `100200` lands on T1110, `100201` on T1078 — two adjacent cells of the
kill chain, so the Grafana matrix shows the SOC covers both the attempt and the breach, not
just the noise of failed logins.

**The test pair.** Fire-on-malicious: a replayed auth log of nine failures then a success
from one IP raises both alerts. Silent-on-benign: a user fat-fingering a password twice then
succeeding raises neither, because two failures sit under the threshold of eight.

**The tuning.** Baselining over a week surfaces two benign-true-positive sources: a
monitoring probe that opens and drops SSH (failures, never a success) and an automation host
doing rapid legitimate logins. The probe is scoped out by its `srcip`; the automation host
is excluded from `100201` by identity (its rapid *successes* are authorized) while still
watched by `100200`. The window and count (eight in 120s) are set from the baseline's
observed failure rate, not a guess — high enough to clear normal retries, low enough to
catch a real spray. Measured precision over the tuned baseline clears the paging bar, so the
rule pages; had it not, it would ship to a dashboard panel in alert-only mode instead.

The triage of a fired T1078 alert — confirming the takeover and deciding whether to isolate
the source — runs through the [operations triage workflow](operations.md#triage-workflow),
and any host isolation is approval-gated per the
[operations response-gating section](operations.md#active-response-the-approval-gate). The
detection logic, its mapping, and its test pair are authored as code, reviewed, and grounded
in the foundation doctrine's
[Kaizen](../../../meta/foundation/SKILL.md) — every false positive that slips through becomes
a new tuning fixture, so the same noise never returns twice.
