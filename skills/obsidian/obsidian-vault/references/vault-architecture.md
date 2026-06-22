# Vault architecture

The vault is a durable, source-backed memory layer for an LLM agent: a folder of
plain Markdown notes that opens in Obsidian as an ordinary vault and reads as a
clean knowledge base for a human. The compiler's job is to turn raw sources
(chat exports, emails, connector output, documents) into that knowledge base
without inventing facts and without losing the trail back to the source.

This page defines the memory model, the note formats, the redaction policy, and
the ingestion tiers. The compilation process that produces them is in
[compiler-process.md](compiler-process.md). The doctrine these choices inherit —
predictability over cleverness — is the [foundation](../../../meta/foundation/SKILL.md),
and the review depth bar is [code-review](../../../engineering/code-review/SKILL.md).

## The four memory types

A useful agent memory separates what it *knows* from how it *acts*, and keeps the
evidence for both:

1. **Declarative memory** — entities and facts. People, Companies, Projects,
   Products, Topics, Decisions. "Ada prefers async standups." Each fact is a
   claim with a source and a confidence.
2. **Procedural memory** — how things are done and what is preferred. Procedures
   ("how we cut a release") and Preferences ("Lucas wants negative conclusions
   stated first"). These steer the agent's behavior.
3. **Source traces** — the raw provenance. One note per ingested source under
   `Sources/`, recording where a fact came from so any claim can be audited back
   to its origin.
4. **Context packs** — pre-assembled briefings. A context pack stitches the
   declarative and procedural notes relevant to one recurring task into a single
   note the agent loads at the start of that task, so retrieval is one read, not
   a graph walk.

Connectors are the fifth concern — not a memory type but the gated doorway
through which external sources enter. Every connector is recorded in
SOURCE-MANIFEST.md before it is read; see "Connector records" below.

## The folder structure

```
<vault>/
  People/          Companies/       Projects/        Products/
  Topics/          Decisions/       Commitments/     Procedures/
  Preferences/     Context Packs/   Sources/         Maps/
  Reports/         _tools/
  README.md            SOURCE-MANIFEST.md   VALIDATION-REPORT.md
  COMPLETION-AUDIT.md  INGESTION-LOG.md     state.json
```

- **Canonical knowledge** lives in the nine domain folders (People … Preferences).
  Each note is one entity or one fact-cluster, source-backed.
- **`Sources/`** holds one note per ingested source — the provenance layer.
- **`Context Packs/`** holds the assembled briefings.
- **`Maps/`** holds Maps of Content (MOCs): index notes that link related
  canonical notes so the graph is navigable.
- **`Reports/`** holds the compiler's own output — ORIENTATION-REPORT.md and any
  per-phase reports.
- **`_tools/`** holds a copy of the validator scripts so the vault re-validates
  on its own after the compiler has moved on.
- The six root control files are the resumable state and the audit trail.

## Note formats

Every canonical note carries YAML frontmatter, a body of source-backed claims,
and a provenance section. The frontmatter is the machine-readable contract; the
body is the human-readable knowledge.

### Person note

```markdown
---
type: person
aliases: [Ada, Countess Lovelace]
tags: [person, collaborator]
status: active
confidence: high
sources:
  - [[Sources/gmail-2026-06-ada-thread]]
  - manifest:gmail-personal
updated: 2026-06-22
---

# Ada Lovelace

Collaborator on the Analytical Engine project. Prefers async standups over
synchronous meetings (confidence: high, two independent sources).

Reportedly fluent in French — single source, unconfirmed (confidence: low).

## Relationships
- Works with [[Charles Babbage]] on [[Analytical Engine]].

## Sources
- [[Sources/gmail-2026-06-ada-thread]] — async-standup preference.
- [[Sources/notion-team-roster]] — role and relationships.
```

### Decision note

```markdown
---
type: decision
tags: [decision, architecture]
status: accepted
date: 2026-05-10
confidence: high
sources:
  - [[Sources/slack-arch-channel-2026-05]]
updated: 2026-06-22
---

# Decision: adopt event-driven sync between billing and ledger

## Context
Cross-service calls coupled billing to ledger latency (per
[[Sources/slack-arch-channel-2026-05]]).

## Decision
Replace the synchronous call with a domain event.

## Consequences
- Looser coupling; eventual consistency the ledger must tolerate.

## Sources
- [[Sources/slack-arch-channel-2026-05]] — the thread where this was agreed.
```

### Context pack note

```markdown
---
type: context-pack
task: "weekly-investor-update"
tags: [context-pack]
confidence: medium
sources:
  - manifest:notion-workspace
updated: 2026-06-22
---

# Context pack: weekly investor update

Load before drafting the investor update.

## Who
- [[People/Ada Lovelace]] — lead, async preference.

## Decisions in force
- [[Decisions/adopt-event-driven-sync]]

## Preferences
- [[Preferences/investor-update-tone]] — numbers first, no hedging.

## Open commitments
- [[Commitments/ship-billing-v2-by-q3]]

## Sources
- manifest:notion-workspace — roster, roadmap, prior updates.
```

### Source trace note

```markdown
---
type: source
connector: gmail
account: lucasatab@gmail.com
captured: 2026-06-22T10:00:00Z
sensitivity: personal
manifest:
  - gmail-personal
---

# Source: Gmail thread "Standup cadence" (2026-06)

Summary of the thread, not a verbatim copy. Ada states a preference for async
standups; Babbage agrees. No credentials, no private contact details copied.
```

## Frontmatter contract

| Key | Meaning | Required on canonical notes |
|-----|---------|------------------------------|
| `type` | note class (person, company, decision, …) | yes |
| `sources` / `provenance` | list of `[[Sources/…]]` links or `manifest:<id>` | yes |
| `confidence` | high / medium / low — the weakest claim sets the floor | yes |
| `aliases` | alternate names Obsidian resolves links by | when the entity has them |
| `status` | active / archived / accepted / superseded | recommended |
| `updated` | ISO date of the last compile touch | yes |
| `sensitivity` | public / internal / personal / restricted | on any source-derived note |

## Representing uncertainty and never inventing facts

The compiler's cardinal rule: a note states only what a source supports. Three
mechanics enforce it:

- **Confidence per claim.** A claim backed by one source is `low`; corroborated
  by two independent sources, `high`. The note's frontmatter `confidence` is the
  minimum across its claims.
- **Explicit unknowns.** A gap is written as a gap ("role unknown — not in any
  source"), never filled by inference. An invented fact is a defect the critic
  pass and `validate-sources` exist to catch.
- **Single-source flags.** A claim from one unverified source carries an inline
  "single source, unconfirmed" marker so a reader weights it correctly.

## Redaction policy

The vault is compiled from the exact places live secrets leak from, so redaction
is a hard gate, not a courtesy:

- **Never copy a secret.** API keys, tokens, private keys, passwords, bearer/OAuth
  tokens, database URLs with inline credentials, SSH keys, webhook/signing
  secrets, and session cookies are never written to a note. `scan-secrets.py` is
  the backstop; the author is the first line.
- **Summarize sensitive content, never paste it.** A source note records *what a
  source says*, not a verbatim dump. Personal data (home address, medical
  detail, private financial figures) is summarized to the minimum the memory
  needs, or omitted.
- **Mark sensitivity.** Every source-derived note carries a `sensitivity` field.
  A `restricted` note names the constraint ("share only with the named party").
- **Redact in place with a marker.** Where a quoted line would carry a secret,
  the secret is replaced by `[REDACTED: <kind>]` so the structure survives and
  the omission is visible.

## Ingestion plan tiers

Sources are ingested in tiers, cheapest-signal and lowest-risk first, so the
HARD CHECKPOINT after the smoke pass reviews a representative slice before the
bulk lands:

1. **Tier 0 — local, already-present sources.** Files in the working directory,
   pasted text, exports the user already handed over. No connector, no external
   call. Always first.
2. **Tier 1 — verified read-only connectors.** Gmail, Notion, Calendar, and
   similar, each gated through SOURCE-MANIFEST.md with account verified and
   read-only capability confirmed. Read, never write.
3. **Tier 2 — broad connector sweeps.** Larger historical pulls (full mailbox,
   whole workspace) run only after the Tier 1 smoke pass is approved at HARD
   CHECKPOINT 2.
4. **Tier 3 — derived and cross-source synthesis.** Context packs and Maps of
   Content, built once enough canonical notes exist to stitch together.

External writes or mutations (sending mail, editing a Notion page, creating a
calendar event) are out of scope for compilation and require separate, explicit
per-action approval — the connector gate records read capability only.

## Connector records

Before a connector is read, SOURCE-MANIFEST.md gets a block with: `id`,
`account`, `workspace`, `verified` (the account was confirmed to be the right
one), `timestamp`, `capability` (read-only for compilation), and `approval`.
A connector whose account does not match the user's intended account is BLOCKED:
no ingestion until the mismatch is resolved. `generate-manifest.py --verify`
checks every connector in `state.json` against this contract.
