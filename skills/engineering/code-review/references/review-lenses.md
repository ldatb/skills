# Review lenses

A tech lead reviews a change against **what it must deliver** and **how it fits the
system** first, and against line-level correctness second. The deterministic gates
(`skill-gate --strict`) already own formatting, lint, types, SAST, SCA, secrets, and
tests — do not re-review those by hand. Spend judgment on what no tool can see.

The lenses are ordered by weight. For a tech lead, lenses 1–4 carry the most leverage:
a change can be locally flawless and still be the wrong thing, in the wrong place.

## 1. Delivery — does it solve the real problem?

The highest-weight lens. Code that is perfect but solves the wrong problem is a blocker.

- Does the change satisfy the stated requirement or acceptance criteria *in full*?
- Is anything in scope missing? Anything out of scope smuggled in?
- Does it handle the real inputs the requirement implies, not only the demo path?
- Would the person who asked for this agree it is done?

Red flags: no linked requirement or decision; "while I was here" changes; a feature that
demos but misses an acceptance criterion; a fix for a symptom, not the cause.

## 2. Architecture & system fit

- Does the change respect existing boundaries (layers, modules, services), or reach across them?
- Dependency direction: does it point toward stable abstractions, or create a cycle?
- Coupling and cohesion: does it bind things that should vary independently?
- Blast radius: what breaks if this is wrong, and is that risk contained?
- Does it follow the grain of the system, or fight it? A change that fights the architecture is a future migration someone inherits.

Red flags: a new pattern competing with an established one; business logic in a
controller or view; a module importing "upward"; a shared mutable singleton; a
cross-service call where an event belongs.

## 3. Conceptual integrity

- Does it reuse an existing concept, or introduce a second way to do the same thing? One concept, one representation.
- Are names drawn from the domain language, consistent with the rest of the codebase?
- Does it preserve the mental model a reader already holds, or force a new one for no gain?

Red flags: a parallel mechanism beside one that already exists; domain terms used
inconsistently; an abstraction named after its implementation rather than its role.

## 4. Abstraction level

- Is the abstraction proportional to the problem?
- Over-abstraction: a framework, factory, or config layer for a single caller (speculative generality).
- Under-abstraction: one concept copied across several sites that will drift apart.
- Is the seam in the right place — hiding what changes, exposing what is stable?

Red flags: an interface with one implementation; a "manager" or "helper" with no single
responsibility; copy-paste with small edits; a premature plugin system.

## 5. Correctness

Now that the change solves the right problem in the right place:

- Edge cases: empty, boundary, large, concurrent, malformed input.
- Errors handled at every level; nothing silently swallowed.
- Invariants preserved; state transitions valid.

Red flags: happy-path only; a broad catch that hides failure; off-by-one; mutation of
shared state.

## 6. Security

- External input validated at the trust boundary.
- No secrets in the diff; queries parameterized; output encoded; authorization on every new action.

Red flags: trust of external data; string-built queries; missing authz; a secret in a fixture.

## 7. Tests

- Does every new behavior have a test that fails without the change?
- Do the tests assert behavior, not implementation? Are the failure paths covered?
- For an architectural change, is the *contract* tested rather than the wiring?

Red flags: tests that still pass with the code commented out; happy-path only; snapshot-only assertions.

## 8. Operability

- Observability: can a failure be diagnosed in production from logs, metrics, or traces?
- Failure modes and rollback: what happens on partial failure, and can this be reverted safely?
- Performance within the budget the intent implies.

Red flags: no logging on a new failure path; an irreversible migration with no plan; a silent N+1.

## Severity

- **blocker** — wrong problem, wrong place, insecure, or unsafe to operate. Stops the merge.
- **major** — a real defect or design risk to fix before release.
- **minor** — advisory: naming, local style, a non-blocking improvement.

Tie every finding to the lens it failed and, for blockers and majors, to the intent it
endangers. A finding the author cannot act on is not a finding — it is noise.
