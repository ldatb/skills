# Compiler process

The vault is *compiled*, not hand-written: raw sources go in one end, source-backed
canonical notes come out the other, and deterministic validators gate the result.
This page is the depth behind the SKILL.md procedure — the nine-stage pipeline,
how entities are canonicalized and deduplicated, which model tier does which
stage, the failure modes, and a worked example.

The depth bar is [code-review](../../../engineering/code-review/SKILL.md): mechanical
correctness is the floor, conceptual integrity is the leverage. The change
discipline — orient, gate, never mutate externally without approval — is the
[git-guardrails](../../../engineering/git-guardrails/SKILL.md) posture applied to
memory. The note formats and redaction policy live in
[vault-architecture.md](vault-architecture.md).

## The nine-stage pipeline

Each source batch flows through these stages in order. A stage consumes the prior
stage's output and produces a checkable artifact.

1. **Parse.** Read the raw source into structured units: messages, emails,
   paragraphs, rows. Strip transport noise (signatures, quoted reply chains,
   boilerplate). Output: a list of clean text units, each tagged with its source
   id and position. Checkable: every unit traces to a source id.

2. **Thread / group.** Cluster units that belong together — a mail thread, a
   chat conversation, a document section. Memory is built from conversations, not
   isolated lines. Output: groups, each a coherent discussion. Checkable: no
   orphan units outside a group.

3. **Classify.** Label each group by the entity type it concerns (person,
   company, decision, preference, …) and the candidate entities it names. Output:
   each group tagged with a type and a candidate-entity list. Checkable: every
   group has a type or an explicit "no canonical content" mark.

4. **Extract.** Pull the atomic claims from each group: subject, predicate,
   object, and the source span that supports it. "Ada → prefers → async standups
   [span 14–18]." Output: a claim list with spans. Checkable: every claim cites a
   span; no claim without a source.

5. **Canonicalize.** Resolve each candidate entity to a single canonical identity
   (see "Entity canonicalization" below). Merge duplicates; pick the canonical
   name; collect aliases. Output: a map from mentions to canonical entities.
   Checkable: no two canonical entities share a normalized name.

6. **Rehydrate provenance.** For every claim, write or update the matching source
   trace note under `Sources/`, and record the connector in SOURCE-MANIFEST.md if
   not already present. Output: source notes exist for every claim's origin.
   Checkable: `validate-sources.py` finds no unresolved ref.

7. **Author.** Write the canonical note: frontmatter, body claims with confidence,
   provenance section. If the canonical note already exists, **update it** —
   append new claims and new provenance, raise confidence where a second source
   corroborates — never create a duplicate. Output: canonical notes written via
   atomic write. Checkable: one note per canonical entity.

8. **Validate links.** Resolve every `[[wikilink]]` to a real note. Fix or flag
   unresolved and ambiguous links. Output: a wikilink report. Checkable:
   `validate-wikilinks.py` exits 0.

9. **Critic / audit.** A separate pass re-reads each new note against its sources
   and asks: is every claim supported? Any invented fact? Any secret copied? Any
   confidence overstated? Output: COMPLETION-AUDIT.md. Checkable: the audit lists
   zero unsupported claims and zero copied secrets.

## Entity canonicalization and dedup

The hardest stage. "Ada", "Ada Lovelace", "A. Lovelace", and "the Countess" must
collapse to one note; "Apple the company" and "apple the fruit" must not.

- **Normalize for matching.** Casefold, trim, and strip honorifics to form a match
  key. `validate-slugs.py` uses the same casefold so the on-disk filename and the
  match key agree.
- **Alias capture, not renaming.** When a new mention matches an existing entity,
  add it to that note's `aliases` — do not rename the note. Obsidian resolves
  links through aliases, so every historical reference keeps working.
- **Type guards the merge.** Two mentions merge only if they share an entity type.
  A person named "Apple" never merges into the company.
- **Ambiguity is surfaced, not guessed.** When a mention could be two entities and
  the sources do not disambiguate, the compiler writes the claim under the more
  specific match and flags it for the critic pass — it never silently picks one.
- **Update over duplicate.** Stage 7 reads the existing note first. A second
  source for an existing claim raises its confidence and appends a provenance
  line; it does not spawn `Ada Lovelace 1.md`.

## Model tiering

The [foundation](../../../meta/foundation/SKILL.md) determinism ladder says: push
work down to scripts, hand the model only the irreducibly stochastic part. Within
the model work, tier by difficulty to control cost without losing quality:

- **Cheap / fast model — parse, thread, classify, extract.** High-volume,
  low-judgment, structurally constrained. The output is checkable (spans, types),
  so a cheaper model's errors are caught downstream. This is where the token
  budget is spent, so it is where the cheap model earns its keep.
- **Strong model — canonicalize, author, critic.** Identity resolution, prose
  authoring, and the adversarial audit need the strongest reasoning. The critic
  pass in particular must be a strong model and should be a *separate* invocation
  from the author, so it does not rubber-stamp its own work.
- **No model — validate.** Stages 8 and the gates are scripts. Determinism owns
  the verdict; the model never decides whether a link resolves.

## Failure modes

| Failure | Symptom | Guard |
|---------|---------|-------|
| Invented fact | A claim with no supporting span | Stage 4 span requirement; critic pass; `validate-sources.py` |
| Duplicate entity | `Ada.md` and `Ada Lovelace.md` both exist | Stage 5 canonicalization; `validate-slugs.py` duplicate class |
| Copied secret | An API key sits in a source note | Redaction policy; `scan-secrets.py` hard gate |
| Broken graph | A `[[wikilink]]` resolves to nothing | `validate-wikilinks.py` unresolved class |
| Placeholder provenance | `source: TODO` shipped | `validate-sources.py` placeholder-ref class |
| Wrong-account connector | Vault built from the wrong mailbox | Connector gate; `generate-manifest.py --verify` |
| Confidence inflation | One source, marked `high` | Critic pass re-reads sources against confidence |
| Lost resumability | A crash mid-batch loses progress | `state.json` + INGESTION-LOG.md updated per batch |

## Red flags

- A canonical note with no `## Sources` section and no `sources:` frontmatter.
- A note that reads more confidently than its single low-confidence source.
- A second note for an entity that already has one — a dedup miss.
- A source trace that quotes a credential, an OTP, or a full home address.
- A connector read before its SOURCE-MANIFEST.md block exists.
- A "smoke pass" that ingested the whole mailbox instead of a representative slice.
- A critic pass run by the same invocation that authored the notes.

## Worked example: compiling one person from one source

**Source:** a Gmail thread, captured as `Sources/gmail-2026-06-ada-thread.md`,
sensitivity `personal`.

1. **Parse** — strip the reply chain and signature; keep three message bodies,
   each tagged `gmail-2026-06-ada-thread:msg-N`.
2. **Thread** — the three messages form one group (subject "Standup cadence").
3. **Classify** — type `person`; candidate entities: "Ada", "Charles".
4. **Extract** — claim `Ada → prefers → async standups`, span `msg-1:14–18`;
   claim `Charles → agrees`, span `msg-2:3–6`.
5. **Canonicalize** — "Ada" matches existing `People/Ada Lovelace.md` (alias
   "Ada" already present). "Charles" matches `People/Charles Babbage.md`. No new
   entities; no duplicates created.
6. **Rehydrate** — the source note already exists; confirm `gmail-personal` is in
   SOURCE-MANIFEST.md with account verified and read capability.
7. **Author** — open `People/Ada Lovelace.md`. The async-standup claim is new and
   now has a *second* source, so its confidence rises `low → high` and a
   provenance line is appended. The note is rewritten via atomic write. No
   duplicate note is created.
8. **Validate links** — `[[Charles Babbage]]` and `[[Analytical Engine]]` both
   resolve; `validate-wikilinks.py` exits 0.
9. **Critic** — a separate strong-model pass confirms: both claims supported by
   cited spans, no invented facts, no secret in the source note, confidence now
   justified by two independent sources. COMPLETION-AUDIT.md records the note as
   clean.

Result: one updated canonical note, one confirmed source trace, one manifest
entry, and a green run from all six validators — no duplication, full provenance,
no invented facts.
