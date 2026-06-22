# Completeness rules

Complete output is the contract: the deliverable carries the whole of what was asked, written out, with nothing deferred and nothing dropped. The model's strongest pull is toward the convenient abbreviation — an ellipsis where ten lines belong, a "similar to above" where the work belongs. This reference names the contract, catalogs the banned shortcuts, gives the protocol for genuinely large output, ties the standard to verification, lists the failure modes and red flags, and closes on a worked contrast.

## The completeness contract

Three obligations, each checkable against the artifact itself.

- **Every requested item delivered in full.** The request names a set — files, functions, endpoints, list entries, sections. The contract delivers that whole set, each member with a real body, not a heading over a promise. A request for seven items answered with five is a breach even when the five are excellent.
- **Every file written end to end.** A file handed back is the complete file: imports through final line, no region replaced by a comment that says the region exists elsewhere. A reader copies the artifact and runs it; a gap that says "rest unchanged" makes the artifact a diff masquerading as a file.
- **Every list enumerated.** A list of N reasons, N steps, or N cases contains N entries spelled out. The convenient tail — a trailing "et cetera", or "the others follow the same pattern" — drops the items the reader most needs spelled out, because the pattern is exactly where readers get the edge cases wrong.

The contract is satisfied only when the artifact, read cold by someone without the conversation, contains everything the request asked for.

## Banned shortcuts

Each shortcut below substitutes a token of work for the work. Each is a defect, never a style choice.

- **Ellipsis-omission in code.** A `...`, a `// ... rest of the code`, a `# (remaining methods unchanged)`, or any comment that stands in for lines the request asked to see. The reader cannot run an ellipsis. When code is the deliverable, the code is present in full.
- **"Fill in the rest."** Any hand-off of the remainder to the reader — "fill in the rest", "complete the implementation", "left as an exercise", "you can add the rest". The remainder was the assignment.
- **"Similar to above."** A pointer used in place of content — "similar to above", "same as the previous one", "analogous to X". The seventh case is named because the seventh case differs; a pointer hides exactly the difference that earns the seventh case its place in the list.
- **Silent dropping of items from a list.** A requested set returned smaller than requested, with no note that anything was cut. Silent shrinkage is the most dangerous shortcut, because the reader cannot see what is missing — the gap leaves no mark.
- **Stubbed functions presented as complete.** A signature with a `pass`, a `return null`, a `throw new NotImplementedError`, or a one-line not-yet-implemented marker as the body, handed back as though the function were finished. A stub is an honest placeholder when labeled a stub and a defect when labeled done.

## Handling genuinely large output

Large output is not a license to truncate. Size is a packaging problem, solved by splitting; truncation is a completeness failure, never solved.

- **Split, do not shrink.** Output too large for one message divides across several files or several messages. Each piece is whole on its own — a complete file, a complete function, a complete section — with no piece trailing into an ellipsis.
- **State what remains, then continue.** Each partial hand-off names the remainder explicitly: "files 1–3 of 8 below; 4–8 follow". The next turn delivers the next whole pieces. The work proceeds until the checklist from the procedure is exhausted.
- **Never fake completion.** A summary is not the artifact. "I've implemented all eight modules" with three shown and five described is the failure this skill exists to stop. The claim of completion matches the delivered bodies, count for count.

The test: concatenate the pieces. The concatenation equals the complete deliverable, with no seam papered over by an ellipsis and no member of the set missing.

## Link to verification-before-completion

Completeness is one face of a single principle: **claimed done equals observed done.** A completion claim is a hypothesis about the artifact, confirmed by reading the artifact — not by recalling the intent.

- A function asserted "implemented" carries a real body in the deliverable, observed, not a stub recalled as finished.
- A list asserted "complete" survives a count against the request, observed, not a count assumed from memory.
- A file asserted "written" reads end to end, observed, not a file whose middle was replaced by "unchanged".

Verification-before-completion forbids declaring success without observing it. Full-output enforcement is that rule applied to the shape of the deliverable: the observation is a scan for omission markers and a count of delivered against requested.

## Failure modes

- **Lazy truncation.** The body exists in the model's plan but never reaches the page; an ellipsis or a "rest unchanged" stands in its place. The cause is economy of effort, and the cure is the step-4 scan.
- **Scope-shrinking.** The delivered set quietly contracts from the requested set — eight became five, the hard three dropped. The cause is the difficulty gradient: the omitted items are usually the hardest. The cure is the step-5 count.
- **Declaring partial work complete.** Prose announces "done" over an artifact that is not. The cause is conflating the intent with the result. The cure is the step-6 check that each completion claim has an observable body.

## Red flags

- A code block contains `...`, "rest of", "remaining", a trailing "et cetera", or a comment substituting for lines.
- The prose says "similar", "analogous", "same pattern", "you can", "simply add", or "left as an exercise".
- A requested count and a delivered count disagree, with no note explaining the gap.
- A function body is a single `pass`, `return null`, `throw`, or a not-yet-implemented marker, under a claim that the function is finished.
- A summary asserts completion that the shown artifact does not contain.
- A list ends early on the entries that look tedious or repetitive.

## Worked example: truncated vs complete

Request: "Write the four CRUD handlers for a `Note` resource."

### Truncated deliverable (a breach)

```python
def create_note(payload):
    note = Note(title=payload["title"], body=payload["body"])
    db.session.add(note)
    db.session.commit()
    return note

def get_note(note_id):
    return Note.query.get_or_404(note_id)

# update_note and delete_note follow the same pattern — fill in as above
```

Three defects in eight lines: two of the four handlers are absent (silent list-dropping); a comment stands in for the missing bodies (ellipsis-omission and "fill in"); and "follow the same pattern" hides the real differences — `update_note` mutates and re-validates, `delete_note` returns a status with no body. The pattern claim is false precisely where it matters.

### Complete deliverable (the contract met)

```python
def create_note(payload):
    note = Note(title=payload["title"], body=payload["body"])
    db.session.add(note)
    db.session.commit()
    return note, 201

def get_note(note_id):
    return Note.query.get_or_404(note_id), 200

def update_note(note_id, payload):
    note = Note.query.get_or_404(note_id)
    note.title = payload["title"]
    note.body = payload["body"]
    db.session.commit()
    return note, 200

def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return "", 204
```

Four requested, four delivered, each body written end to end. The count matches, no ellipsis stands in for a body, and no handler is a stub wearing the label "done". The deliverable runs as written; the reader supplies nothing the request asked the author to supply.
