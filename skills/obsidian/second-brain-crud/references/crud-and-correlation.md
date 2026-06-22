# CRUD and correlation in a second brain

The judgment behind the second-brain-crud steps. A second brain earns its keep only
when capture is frictionless and the pieces connect. This reference inherits the
[foundation](../../../meta/foundation/SKILL.md) doctrine — predictability over
cleverness, a script over freehand file edits — and borrows the tech-lead depth bar
from [code-review](../../../engineering/code-review/SKILL.md): judge the vault against
what it must deliver (fast recall of connected context), not only whether each note is
individually tidy.

The vault is shared state across your whole life and work. Every mutation runs through
`scripts/vault.sh`, so a note is never half-written, a filename never overwrites, and the
single delete path refuses anything but one file inside the vault root.

## The note-type taxonomy

Eleven types cover personal life, job, projects, and the management surface (clients,
feedback, 1:1s, companies). One uniform frontmatter block sits on every note (so
correlation queries stay simple), and the type adds its own fields and heading set on top.

| Type | Captures | Type-specific frontmatter | Headings |
|------|----------|---------------------------|----------|
| `person` | a human you interact with | `company`, `role` | Notes, Related |
| `project` | a sustained effort with an outcome | `status`, `owner` | Notes, Related |
| `meeting` | a conversation and its outcomes | `date`, `attendees` | Notes, Decisions, Action items, Related |
| `idea` | a seed worth keeping | `status` | Notes, Related |
| `task` | a discrete unit of work | `status`, `due` | Notes, Related |
| `decision` | a choice and its reasoning | `date`, `status` | Context, Decision, Consequences, Related |
| `daily` | one day's running log | `date` | Log, Tasks |
| `client` | a client relationship and its health | `status`, `company` | Notes, Related |
| `feedback` | one SBI feedback instance | `date` | Notes, Related |
| `1on1` | one direct-report 1:1 session | `date` | Notes, Action items, Related |
| `company` | an organization you track | `industry` | Notes, Related |

Shared frontmatter on every note: `title`, `type`, `created`, `tags`. The `type` value
also seeds the first tag, so `vault.sh find "tags: [project]"` enumerates one type
deterministically. These four shared keys are owned by the template and cannot be set as
capture fields, which keeps the correlation queries stable.

### Setting fields at capture

`vault.sh capture <type> "<title>" key=value ...` writes each trailing `key=value` as a
frontmatter field, so a note lands with its custom fields already set — no follow-up edit,
no hand-typed YAML. The rules the script enforces:

- The key is a simple identifier (`[a-z_]+`); anything else is rejected at the boundary.
- The value is emitted bare, and wrapped in double quotes when it carries a `:` or `#`
  (or a quote, backslash, or edge whitespace), so the YAML stays valid.
- A key matching a type default *replaces* that default, so the field never duplicates —
  `capture project "Roadmap" owner=lucas` yields a single `owner: lucas`.
- Sensitivity is a capture field: `capture feedback "SBI for Ada" sensitivity=private`
  marks the note private at creation, the discipline the management skills rely on.
- Fields are validated before any file is reserved, so a bad field aborts the capture
  with no orphan note left behind.

## The capture-fast principle

A second brain that is slow to write to does not get written to. Friction is the enemy,
and the antidote is a single command per thought:

- One verb, two arguments: `vault.sh capture <type> "<title>"` returns a ready note path;
  optional trailing `key=value` args set frontmatter fields in the same call.
- The slug is derived from the title by the script, never typed by hand.
- The filename is reserved collision-free (noclobber `set -C`, the shell's O_EXCL),
  so two notes titled "Sync" never overwrite — the second becomes `sync-2.md`.
- A passing thought goes to today's note: `vault.sh daily` then `vault.sh append`.

Capture first, organize later. A rough note that exists beats a perfect note you never
wrote. Correlation and cleanup are a separate, lower-frequency pass.

## Correlation patterns

A pile of notes is not a second brain; a *graph* is. Correlation is what turns isolated
capture into recall. Three mechanisms, in order of strength:

### 1. Wikilinks between entities

The backbone. `vault.sh link <from> <to>` adds a `[[wikilink]]` under the source note's
`## Related` section, and the link is idempotent (a repeat is a no-op). Link entities
along the natural relations of work and life:

- person ↔ project — who is on what.
- person ↔ company — who works where.
- meeting ↔ person — who was in the room.
- meeting ↔ project — what the meeting moved.
- decision ↔ project — what a choice changed.
- decision ↔ person — who owns the call.

Obsidian renders these links bidirectionally in its graph and backlinks pane, so one
`link` call surfaces both notes from each other.

### 2. Tags for cross-cutting themes

Links join two named things; a tag groups many notes under a theme that has no single
home note — `#hiring`, `#q3`, `#health`. Add tags to the frontmatter `tags` list. A tag
answers "everything about X" where X is an axis, not an entity.

### 3. MOC / index notes

A Map of Content is a hand-curated `project`-or-`idea` note whose `## Related` section
links the notes that matter for one area — a person's dashboard, a project's hub, a
domain's table of contents. An MOC is the entry point a search cannot replace: it
encodes *which* links matter, in *what* order, with *your* framing.

## Keeping the vault navigable

A graph that nobody can traverse is noise. The navigability bar:

- Every entity worth recalling has at least one inbound or outbound link.
- A new project gets an MOC on day one, then accretes links as the work proceeds.
- Daily notes funnel transient capture; durable entities get their own typed note.
- Frontmatter stays uniform, because the search depends on it.

## Failure modes

| Failure | Symptom | Cause | Fix |
|---------|---------|-------|-----|
| Orphan notes | a note with no links, found only by full-text search | capture without correlation | a `link` pass; an MOC for the area |
| Inconsistent frontmatter | a tag query misses notes that belong | hand-edited YAML drifting from the template | capture through `vault.sh`, which renders uniform frontmatter |
| Duplicate entities | two `person` notes for one human | re-capture instead of reuse | `vault.sh find` before capture; merge, then delete one via `vault.sh rm` |
| Capture friction | thoughts never reach the vault | a heavyweight ritual per note | the one-command capture path; defer organizing |
| Link rot | a wikilink points at a renamed note | a note renamed outside the script | rename through the vault, relink the source |

## Red flags

- A note created by hand-editing a file instead of `vault.sh capture` — the slug and the
  collision guard are skipped, and a future capture may overwrite it.
- A timestamp baked into a filename to dodge collisions — that is the job of the
  reservation loop, not of a human-typed name.
- A growing set of orphan notes — capture is outrunning correlation; schedule a link pass.
- A bulk-delete instinct ("clear out the old notes") — the only supported delete is one
  guarded file at a time through `vault.sh rm`, by design.
- Frontmatter typed differently on two notes of the same type — the query layer quietly
  loses one of them.

## Worked example: a meeting, linked to a person and a project

The scenario: a kickoff meeting with Ada Lovelace about the Q3 Roadmap project.

1. Capture the meeting note:

   ```sh
   vault.sh capture meeting "Kickoff sync"
   # -> <vault>/meeting/kickoff-sync.md
   ```

2. Record an outcome as a timestamped bullet under `## Log`:

   ```sh
   vault.sh append <vault>/meeting/kickoff-sync.md "agreed Q3 scope with Ada"
   ```

3. Correlate the meeting to the person and the project (the person note and the project
   note already exist from earlier capture):

   ```sh
   vault.sh link <vault>/meeting/kickoff-sync.md "Ada Lovelace"
   vault.sh link <vault>/meeting/kickoff-sync.md "Q3 Roadmap"
   ```

The meeting note now carries two links under `## Related`:

```md
## Related
- [[ada-lovelace]]
- [[q3-roadmap]]
```

Open the person note in Obsidian and the backlinks pane shows the kickoff meeting; open
the project note and the same meeting appears there. One capture plus two `link` calls
turned a transient conversation into a node the graph can reach from three directions —
the person, the project, and full-text search — which is the whole point of a second
brain.
