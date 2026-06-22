# Engineering practices

The reference behind the build steps. Read the section for the layer you are touching;
each carries a checklist, the red flags that mark a bad change, and a worked example.
The deterministic gates (`skill-gate --strict`) own the mechanical checks — this page is
the judgment they cannot encode.

## Design — the seam

Before code, decide where the change lives and what it exposes. A seam in the wrong
place is the most expensive mistake in the change, because everything built on it
inherits the error.

- **Boundary**: which module/layer/service owns this? Does the change keep behavior on
  the correct side of an existing boundary, or smear it across two?
- **Interface**: what is the smallest surface that does the job? Expose what is stable;
  hide what will change.
- **Dependency direction**: does the new code depend inward toward stable abstractions,
  or does it create a cycle or an upward import?
- **Data shape**: model the data once, at the right altitude. A type that makes an
  illegal state unrepresentable beats a runtime check.

Red flags: a new concept that duplicates an existing one; logic that belongs in the
domain leaking into a controller or view; a "temporary" cross-layer shortcut; a data
model that needs a comment to explain which combinations are valid.

## Backend

Checklist:

- **Contract first**: inputs, outputs, error shape, and the authorization required are
  written before the implementation.
- **Authorization** on every new action, checked server-side, never trusted from the client.
- **Input validation** at the boundary; reject malformed requests before any work runs.
- **Idempotency** for anything a client may retry (payments, writes behind a flaky network).
- **Data integrity**: transactions around multi-step writes; constraints in the database,
  not only in app code.
- **Errors**: a typed, documented error contract; no leaking of internals to the caller.
- **Pagination and limits** on every collection endpoint; no unbounded result sets.
- **Concurrency**: assume two requests race; reserve identifiers atomically, never check-then-write.

Red flags: authorization in the UI only; a list endpoint with no limit; a retry that
double-charges; a 500 that returns a stack trace; string-built SQL.

Worked example — "add a delete-account endpoint": the contract names who may call it
(the owner or an admin), what it returns (202 + a job id), and its error shape
(403, 404). Deletion is a queued, idempotent job, not a synchronous cascade; a second
call returns the same job id. The test asserts a non-owner gets 403 before anything is touched.

## Frontend

Checklist:

- **Accessibility**: every interactive element has a role, an accessible name, and
  keyboard operation; focus is managed on route and modal changes; color is not the only
  signal. Target WCAG AA.
- **The four states**: every async view handles loading, empty, error, and success — not
  only the success path.
- **State**: derive rather than duplicate; a single source of truth for each piece of
  state; no server data mirrored into local state that can drift.
- **Rendering cost**: stable references for props that feed memoized children; no work in
  render that belongs in an effect or a memo.
- **UX correctness**: optimistic updates roll back on failure; forms disable on submit;
  destructive actions confirm.

Red flags: a div with a click handler and no role or key support; a spinner with no
error state; an effect that refetches on every render; color-only validation feedback.

Worked example — "a results list": the component renders a skeleton while loading, an
empty-state with a next action when there are zero results, an error state with a retry,
and the list on success. Each row is reachable and activatable by keyboard. The test
asserts the empty and error states render, not only the populated list.

## Cross-cutting

- **Coupling and cohesion**: things that change together live together; things that vary
  independently are not bound.
- **Observability**: a new failure path emits a log or metric a responder can act on.
- **Performance budget**: state the budget the requirement implies (a request under N ms,
  a bundle under N kb) and check the change against it.
- **Reversibility**: a risky change ships behind a flag or with a rollback path.

Red flags: a new failure path that is silent in production; an N+1 introduced under an ORM;
a migration with no down path; a synchronous call where an event belongs.
