---
name: second-brain-crud
description: Fast, deterministic CRUD and correlation over an Obsidian second-brain vault — capture typed notes, append log entries, link entities into a graph, open the daily note, and search. Use when the user wants to capture a person, project, meeting, idea, task, decision, or daily note; jot something into their vault; connect or correlate notes; link people to projects or companies; or find a note by tag, title, or text.
---

Treat the Obsidian vault as a second brain for personal life, job, and projects. The
value is fast capture plus correlation: a thought lands in one command, and entities
link into a graph that recall can traverse. Every mutation runs through
`scripts/vault.sh`, so a filename never overwrites, a write is never half-finished, and
the lone delete path refuses anything but a single file inside the vault root.

The judgment — the note-type taxonomy, the capture-fast principle, the correlation
patterns, and the failure modes — lives in
[the CRUD and correlation reference](references/crud-and-correlation.md). Read that
reference before a vault session.

The vault root resolves from `$VAULT`, falling back to `./vault`. Types: `person`,
`project`, `meeting`, `idea`, `task`, `decision`, `daily`, `client`, `feedback`,
`1on1`, `company`.

## Steps

1. **Name the operation and the target.** State the verb (capture, append, link, daily,
   find, or remove) and the note the verb acts on, drawn from the user's request. This
   step is done once the verb maps to one `vault.sh` subcommand and the target note is
   named.

2. **Capture through the script.** Create a typed note with
   `scripts/vault.sh capture <type> "<title>" [key=value ...]`, which renders uniform
   frontmatter, derives a safe slug, and reserves a collision-free filename. Each trailing
   `key=value` argument writes one frontmatter field — the key is a simple identifier
   (`[a-z_]+`), the value is quoted automatically when it carries a `:` or `#`, and a key
   matching a type default replaces that default. A field whose key is overridden stays
   single, so `capture project "Roadmap" owner=lucas` yields one `owner: lucas`. Set
   sensitivity at capture with `sensitivity=private`. The reserved structural keys
   `title`, `type`, `created`, and `tags` are set by the template and rejected as fields.
   This step is done once the command prints the new note path.

3. **Append a log entry.** Add a timestamped bullet under the note's `## Log` section with
   `scripts/vault.sh append <note> "<text>"`. This step is done once the command returns
   the note path and the bullet sits under `## Log`, clear of `## Related`.

4. **Correlate entities.** Link the note to a related person, project, company, or decision
   with `scripts/vault.sh link <from> <to>`, which adds an idempotent `[[wikilink]]` under
   `## Related`. This step is done once the relations the request implies exist as links
   and the source note's `## Related` lists them.

5. **Open today's daily note.** Run `scripts/vault.sh daily` for the create-or-open daily
   note. This step is done once the command prints today's daily path, the same path on a
   re-run.

6. **Find a note.** Locate notes by tag, title, or text with
   `scripts/vault.sh find "<query>"`. This step is done once the matching paths are listed,
   an empty result reported plainly.

7. **Remove through the guard.** Delete a single note only with
   `scripts/vault.sh rm <note>`, the one guarded path that refuses the vault root and any
   target outside it. This step is done once the command prints the removed path, or stops
   at the guard with its message.
