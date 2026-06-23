# Documents as a deliverable: the ADR and the design doc

A design that lives only in a meeting dies in that meeting. The two documents that
outlast it are the **ADR** — one significant decision, with its alternatives and
consequences — and the **design doc** — the one-page overview that frames the diagrams
and the ADRs for a reader arriving cold. Both are deliverables of the design process,
emitted in [step 7](design-process.md#decision-procedure).

An ADR records *why one choice won*; a design doc records *what the system is*. The ADR
is the higher-leverage artifact, because the reasoning behind a hard-to-reverse decision
is the thing a future engineer most needs and most often lacks.

## When to write an ADR

One ADR per significant, hard-to-reverse decision — not per task, and not per file
touched. The test for "significant": reversing the choice later would be expensive, or
the choice closes off options a reader might otherwise assume are open. A datastore
class, a sync-vs-async boundary, a monolith-vs-services split, a build-vs-managed call
each clear that bar. A variable name does not.

A choice with an obvious answer and no rejected alternative does not need an ADR; an ADR
with no rejected alternative and no negative consequence is marketing, not a record.

## The ADR template

Copy this template per decision. The fenced block keeps it verbatim:

```markdown
# ADR-NNN: <short noun phrase naming the decision>

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-MMM
**Date:** YYYY-MM-DD
**Deciders:** <names or roles>

## Context

The forces in play: the requirement, the constraints, the ranked quality attributes
that pressure this choice, and the scale numbers that matter. State the problem so a
reader who was not in the room understands what was being decided and why now.

## Decision

The option chosen, stated as one active sentence. Then a short paragraph on how it
works, only as far as the decision needs.

## Alternatives considered

- **<Alternative A>.** What it is, and the one reason it lost.
- **<Alternative B>.** What it is, and the one reason it lost.

## Consequences

- **Positive:** what becomes easier or possible.
- **Negative:** what becomes harder or impossible — the cost accepted. Name at least
  one; a decision with no downside was not a decision.
- **Follow-ups:** the work this decision now requires, if any.
```

The five load-bearing fields:

- **Status** — a lifecycle marker. An ADR is never deleted; a reversed decision is
  marked `Superseded by ADR-MMM`, so the trail of reasoning stays intact.
- **Context** — the forces: the requirement, the constraints, the ranked attributes, the
  numbers. A reader judges the decision against the context, so a thin context makes the
  decision unjudgeable.
- **Decision** — one active sentence. A decision a reader cannot restate in a sentence is
  not yet a decision.
- **Alternatives** — the roads not taken, each with the reason it lost. The alternatives
  are the most valuable field and the one most often skipped.
- **Consequences** — both signs. The negative consequence is the honesty that separates a
  record from a sales pitch.

## The design doc

The design doc is the one-page front matter that orients a reader before the diagrams
and the ADRs. Keep it short — a long design doc goes unread and unmaintained. The
outline:

```markdown
# <System name> — design doc

## Problem and scope
What this system does, and what it explicitly does not do.

## Requirements and constraints
Functional scope, the scale numbers, and the hard constraints
(budget, team, deadline, compliance, residency).

## Quality attributes (ranked)
The two or three dominant attributes, each with a target number.

## Architecture overview
The C4 System Context and Container diagrams, linked or embedded.

## Key decisions
A list linking each ADR, one line of summary apiece.

## Risks and open questions
What could still sink this, and what is not yet decided.
```

The design doc does not repeat the ADRs; it links them. The diagrams are embedded as
` ```mermaid ` blocks or linked from [the C4 diagrams](diagrams-c4-mermaid.md) so the
doc renders as one navigable page.

## Decision procedure

1. **Write one ADR per significant decision.** Use the template above. The step is done
   once each hard-to-reverse choice has an ADR carrying at least one rejected
   alternative and at least one negative consequence.
2. **Number and status every ADR.** Sequential `ADR-NNN`, with a status from the
   lifecycle set. The step is done once each ADR has a unique number and a status.
3. **Write the one-page design doc.** Use the outline above; embed or link the Container
   diagram and list the ADRs. The step is done once the doc fits roughly one page and
   links every ADR.

## Failure modes

- **The decision with no alternative.** An ADR that presents one option as inevitable,
  with no road not taken. Counter: the template's Alternatives field is required, and an
  ADR without it is rejected.
- **The all-upside record.** An ADR whose Consequences list only benefits. Counter: at
  least one negative consequence is mandatory; a decision with no cost was not a
  decision.
- **The novel.** A ten-page design doc nobody reads or updates. Counter: one page, with
  the depth pushed into linked ADRs and diagrams.
- **The deleted decision.** A reversed choice whose ADR was erased, so the next engineer
  re-litigates a settled question. Counter: never delete an ADR; mark it
  `Superseded by ADR-MMM`.
- **The orphan ADR.** A decision record with no link from the design doc, lost in a
  folder. Counter: the design doc's Key decisions section links every ADR.

### Red flags

- An ADR with an empty or absent Alternatives section.
- A Consequences section with no negative entry.
- A design doc longer than two pages.
- An ADR deleted rather than superseded.
- A decision made in a thread or a meeting with no ADR written at all.

## Worked ADR

The central decision from the
[URL shortener](design-process.md#worked-example-the-url-shortener), filled into the
template:

```markdown
# ADR-001: Use a partitioned key-value store as the system of record

**Status:** Accepted
**Date:** 2026-06-23
**Deciders:** Platform tech lead, on-call lead

## Context

The redirect read path dominates (100:1 reads, ~40k reads/sec at peak) and sits on the
user's critical path (p99 < 50ms, 99.99% availability). The store grows ~30 TB over
five years. The only hot online query is a point lookup by short code; no joins or
ad-hoc queries run on the request path.

## Decision

Store the `code -> long_url` mapping in a partitioned key-value store, sharded by code,
fronted by a read-through cache for the hot set. The Write API allocates a base62 code
from a range-leased ID generator; the Read API resolves through the cache and falls
through to the store on a miss.

## Alternatives considered

- **Relational database (single primary + read replicas).** Correct and familiar, but
  sharding 30 TB is heavy operational work and the relational feature set (joins,
  transactions, ad-hoc queries) buys nothing the online path uses. Rejected on cost and
  scalability.
- **Hash the URL for the code instead of a counter.** Deduplicates identical URLs, but
  collision handling adds read-path complexity and identical-URL deduplication is not a
  requirement. Rejected on needless complexity.

## Consequences

- **Positive:** point lookups stay fast and the store scales horizontally by code; the
  cache absorbs peak read volume.
- **Negative:** ad-hoc reporting is impossible on the system of record and moves to a
  separate analytics path; cross-key transactions are unavailable, accepted because no
  flow needs them.
- **Follow-ups:** size the cache to the hot set (~20% of codes); design the ID
  generator's range-lease so it is not a single point of failure.
```

This ADR is checkable: a unique number and a status, a one-sentence decision, two
rejected alternatives each with a reason, and a named negative consequence. Paired with
the [C4 diagrams](diagrams-c4-mermaid.md#worked-example-the-url-shortener), it is the
documentary half of the design's output.
