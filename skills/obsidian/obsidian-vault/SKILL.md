---
name: obsidian-vault
description: Compile a source-backed Obsidian vault — a durable LLM/agent memory layer — from available sources, validated by deterministic scripts. Use when the user asks to build, compile, or refresh an Obsidian memory vault, a second brain, or an agent knowledge base from chats, emails, notes, or connectors; or to ingest sources into a provenance-tracked vault.
---

Compile a durable memory vault the way a build system compiles source: raw
sources go in, source-backed canonical notes come out, and deterministic
validators gate the result. The vault opens as an ordinary Obsidian folder and
reads as a clean knowledge base. Two rules dominate — never invent a fact a
source does not support, and never ship a copied secret.

The pipeline is **resumable** and **gated**. Progress is journaled to
`state.json` and `INGESTION-LOG.md` after every batch, so a crashed or paused run
resumes from the last checkpoint. Two HARD CHECKPOINTS pause for the user before
broad ingestion. The depth bar is [code-review](../../engineering/code-review/SKILL.md);
the determinism doctrine is the [foundation](../../meta/foundation/SKILL.md).

The architecture (memory types, note formats, redaction policy, ingestion tiers)
is in [references/vault-architecture.md](references/vault-architecture.md). The
nine-stage pipeline, canonicalization, model tiering, and a worked example are in
[references/compiler-process.md](references/compiler-process.md).

## Phase 0 — Resume check

1. **Read prior state first.** Look for `state.json` and `INGESTION-LOG.md` at the
   output path. On a resume, read both before any other action, then continue from
   `current_phase` and `next_actions`. The step is done once prior state is loaded,
   or confirmed absent for a fresh compile.

## Phase 1 — Orientation

2. **Inspect the sources.** Enumerate available sources: working-directory files,
   pasted text, and the connectors the user named. Record the working directory,
   the output path, and a source inventory. The step is done once the inventory
   names every source the user expects.

3. **Verify accounts before proposing.** Per external connector, capture which
   account and workspace it is signed into. A connector signed into the wrong
   account is recorded as a blocker, not a source. The step is done once each
   connector has a verified account or a blocker entry.

4. **Write the orientation report.** Produce `Reports/ORIENTATION-REPORT.md`
   holding the working directory, output path, source and connector inventory,
   account verification, the proposed compilation plan, and any blockers. The step
   is done once the report exists and names the plan.

5. **HARD CHECKPOINT 1 — pause for approval.** Present the orientation report and
   stop. Broad ingestion does not begin until the user approves the plan. The step
   is done once the user has approved, amended, or rejected the plan.

## Phase 2 — Connector gate

6. **Record every connector before reading it.** Per connector, write a
   SOURCE-MANIFEST.md block with `id`, `account`, `workspace`, `verified`,
   `timestamp`, `capability` (read-only for compilation), and `approval`. Run
   `scripts/generate-manifest.py --vault <path> --verify` to confirm the contract.
   The step is done once the verifier exits 0.

7. **Block a wrong-account connector.** A connector whose account does not match
   the user's intended account stays blocked: no read, no ingestion, until the
   mismatch is resolved. The step is done once no blocked connector remains in the
   plan. Never perform an external write or mutation without explicit per-action
   approval — compilation reads sources only.

## Phase 3 — Compile

8. **Initialize the vault skeleton.** Create the required folders and control
   files at the output path. Run `scripts/validate-artifacts.sh --vault <path>` to
   confirm the structure. The step is done once the artifact check exits 0.

9. **Run the pipeline per source batch.** Drive each batch through the nine
   stages — parse, thread, classify, extract, canonicalize, rehydrate provenance,
   author, validate links, critic — detailed in
   [references/compiler-process.md](references/compiler-process.md). The step is
   done once every batch in the current tier has a pipeline pass recorded.

10. **Update, never duplicate.** A canonical note that already exists for an entity
    gains appended provenance and raised confidence on corroboration rather than a
    second note. The step is done once no entity owns two canonical notes.

11. **Journal progress per batch.** After a batch, update `state.json`
    (`output_path`, `current_phase`, `completed_phases`, `sources_discovered`,
    `sources_ingested`, `connector_status`, `batches_completed`,
    `canonical_notes_created`, `validation_status`, `next_actions`, `blockers`) and
    append a line to `INGESTION-LOG.md`. The step is done once both reflect the
    batch just finished.

## Phase 4 — Smoke pass and checkpoint

12. **Compile a representative slice.** From Tier 0 and Tier 1 sources only,
    compile a small representative sample across entity types. The step is done
    once at least one canonical note per major type exists.

13. **HARD CHECKPOINT 2 — show the sample, then pause.** Present sample canonical
    notes, one source trace from claim to source, one context pack, the
    SOURCE-MANIFEST.md, and the validation report. Stop. Broad ingestion does not
    proceed until the user approves the sample. The step is done once the user has
    approved or amended the sample.

## Phase 5 — Validate

14. **Run the deterministic validators.** Run each script against the vault:
    `scripts/validate-wikilinks.py`, `scripts/validate-slugs.py`,
    `scripts/scan-secrets.py`, `scripts/validate-sources.py`,
    `scripts/validate-artifacts.sh`, and `scripts/generate-manifest.py --verify`.
    A script's exit code is the verdict — branch on the code, not on its prose.
    The step is done once every validator has run and its result is captured.

15. **Write the validation report.** Record each validator's result in
    `VALIDATION-REPORT.md`. The step is done once the report names every validator
    and its pass-or-fail verdict.

## Phase 6 — Hard gates

16. **Hold the completion gates.** A compile is complete only when all of the
    conditions below hold. A red gate blocks completion: fix the cause, re-run the
    validator, re-check.

    - 0 placeholder source refs — the placeholder-ref class of `validate-sources.py` is empty.
    - 0 broken wikilinks; 0 ambiguous wikilinks left unresolved.
    - 0 empty slugs; 0 invalid paths (no `People/.md`); 0 duplicate slugs.
    - 0 copied secrets reported by the secret scan.
    - Provenance present on each promoted canonical note.
    - Each connector documented in SOURCE-MANIFEST.md with a verified account.
    - `README.md`, `VALIDATION-REPORT.md`, `COMPLETION-AUDIT.md`,
      `INGESTION-LOG.md`, and `state.json` exist.
    - The vault opens as a normal Obsidian folder of plain Markdown.

17. **Write the completion audit.** Produce `COMPLETION-AUDIT.md`: the gate
    results, the count of canonical notes and sources, and any residual
    low-confidence claims. The step is done once the audit records every gate as
    held and the validators as green.

## Required structure

```
<vault>/
  People/          Companies/       Projects/        Products/
  Topics/          Decisions/       Commitments/     Procedures/
  Preferences/     Context Packs/   Sources/         Maps/
  Reports/         _tools/
  README.md            SOURCE-MANIFEST.md   VALIDATION-REPORT.md
  COMPLETION-AUDIT.md  INGESTION-LOG.md     state.json
```

## Scripts

A script runs `--selftest` to build temp fixtures, assert, and exit 0. Each is
read-only against the vault except `generate-manifest.py --generate`:

- `scripts/validate-wikilinks.py` — resolve `[[wikilinks]]`; report unresolved and ambiguous.
- `scripts/validate-slugs.py` — empty filenames, invalid paths, duplicate slugs, unsafe chars.
- `scripts/scan-secrets.py` — credential-shaped strings, reported masked for redaction.
- `scripts/validate-sources.py` — provenance present; every source ref resolves.
- `scripts/validate-artifacts.sh` — required folders and control files present.
- `scripts/generate-manifest.py` — generate or verify SOURCE-MANIFEST.md from `state.json`.
