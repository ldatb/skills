# The project-management system

Project management for a tech lead and founder is the discipline of keeping a goal honest
under change: knowing what the project must deliver, what stands between here and there, and
what the project just learned. The artifact is a **project record** in the Obsidian second
brain, kept deliberately light. The vault is the point — a job project and a personal project
live in the same graph, so people, companies, and commitments correlate across both.

This reference sets the depth bar. Note CRUD — creating notes, writing frontmatter, linking,
querying — belongs to [second-brain-crud](../../../obsidian/second-brain-crud/SKILL.md). This
skill owns judgment: what the record must hold and when its state changes.

The sections are ordered by weight. A project can have an immaculate task board and still be
the wrong project, tracked against nothing.

## 1. The project record

One note per project. The record is the single source of truth; a fact that lives only in
chat or in someone's head is not tracked. The record holds:

- **Goal** — the outcome in one sentence, stated as a result a reader can test ("paid signups
  reach 100", not "improve onboarding"). A goal that names an activity hides whether the
  project is done.
- **Scope** — what is in, and an explicit line for what is out. The out-of-scope line is the
  load-bearing half: scope creep enters through everything left unstated.
- **Milestones** — 3–7 dated checkpoints between now and the goal, each with a done-condition.
- **Status** — one of a small fixed set (planned, active, blocked, done, dropped). A free-text
  status drifts into prose nobody can filter on.
- **Owner** — the single name accountable. Two owners is zero owners.
- **Risks** — what could break the plan, each with likelihood, impact, and an owner.
- **Decisions** — the choices made, each linked to its decision note.
- **Next actions** — the two or three things that move the project this week.

Red flags: a goal phrased as an activity; no out-of-scope line; status as a paragraph instead
of a state; two owners or none; next actions longer than the milestone list.

## 2. Tracking work

A task is a unit of work with a single, observable **acceptance criterion** — the condition
under which the task is done, written before the work starts. "Wire up auth" is not a task;
"a logged-out user hitting /dashboard is redirected to /login" is.

- **One acceptance criterion per task.** A task needing two criteria is two tasks.
- **WIP limits.** Cap work-in-progress (3–5 open tasks for a solo founder is a sane default).
  A low limit forces finishing over starting; unbounded WIP is how ten things sit at 80%.
- **Status cadence.** Update the record on a fixed rhythm — weekly is the default. The cadence
  is what keeps the plan from going stale; a record touched only when convenient lies by the
  second week.
- **Move on done, not on effort.** A task advances when its acceptance criterion is met, never
  because time was spent on it.

Red flags: tasks with no acceptance criterion; a board where everything is "in progress"; the
last update older than one cadence period; "90% done" with no criterion that defines the 90%.

## 3. Planning

Planning turns a goal into a path and an honest estimate of its length.

- **Decompose top-down.** Goal → milestones → the nearest milestone's tasks. Plan the next
  milestone in detail; sketch the rest. Detailed plans for distant milestones are fiction with
  good formatting.
- **Estimate against actuals.** Anchor each estimate on how long a comparable past task took,
  not on how long the work feels. The planning fallacy is the default; past actuals are the
  correction.
- **Dependencies.** Mark which tasks block which. A dependency left implicit becomes a surprise
  on the day it bites.
- **Critical path.** Name the longest chain of dependent tasks — the chain that sets the
  earliest possible finish. Slip on the critical path slips the project; slack elsewhere is
  free. A plan that does not name its critical path cannot say what to protect.

Red flags: a flat task list with no milestones; estimates with no basis in prior work; the
critical path unnamed; every task marked equally urgent.

## 4. Risk and decision logs

**Risks.** A risk is a future event that would damage the plan. Each logged risk carries a
likelihood, an impact, and an owner who watches it. An ignored risk does not stop being a
risk; it stops being visible. Review open risks every cadence — a stale risk log is theater.

**Decisions.** A material decision — an architecture choice, a scope cut, a vendor pick —
goes in its own decision note, linked from the project via
[second-brain-crud](../../../obsidian/second-brain-crud/SKILL.md). The decision note records
the context, the options weighed, the choice, and the consequence accepted. An untracked
decision gets relitigated; the log is what lets the project answer "why did we do it this way"
six months on.

Red flags: a risk with no owner; a risk log that never changes; a major decision visible only
as a code diff; a decision reversed with no note on why.

## 5. Status reporting

A status update has exactly three parts:

- **Changed** — what moved since the last report (tasks done, milestones hit, facts learned).
- **Next** — what the project will do before the next report.
- **Blocked** — what is stuck, and the risk or decision each blocker traces to.

The blocked section is the one that earns the report. An update that lists progress and hides
blockers is **status theater** — it manufactures the feeling of control while the real
obstacles stay invisible until they detonate. When nothing is blocked, the update says "none
blocked" rather than dropping the section.

Keep it short. A status update is a signal, not a essay; three tight sections beat a page of
narrative that buries the one thing the reader needed.

Red flags: progress-only updates; blockers softened into "minor items"; an update so long the
blocker is buried; a report cadence that quietly lapses under pressure.

## 6. Keeping it lightweight

The system serves the work, not the reverse. Every field in the record earns its place by
changing a decision; a field nobody reads is overhead that makes the next update slower and
the whole record likelier to be abandoned.

- Prefer the smallest record that keeps the project honest.
- Add a field when its absence caused a miss, not speculatively.
- A process step that has never caught anything is a candidate to drop.

Red flags: ceremony that outweighs the project; fields filled to satisfy the template, not a
reader; a cadence so heavy the update gets skipped.

## 7. Correlation in the vault

The reason the record lives in the second brain rather than a standalone tracker: correlation.
Link the project to the people on it, the company or client it serves, and the commitments it
satisfies, all through [second-brain-crud](../../../obsidian/second-brain-crud/SKILL.md). Once
linked, a query across the vault answers questions a flat tracker cannot — what is this person
on the hook for, what does this client have in flight, which commitments has this quarter's
work actually advanced. A job project and a personal project in the same graph let the founder
see the whole load, not one silo at a time.

Red flags: a project that links to nothing; people named in prose instead of linked notes; two
projects for the same client with no shared company link; commitments tracked apart from the
projects meant to deliver them.

## Failure modes

- **Status theater** — reporting motion while hiding blockers. The cure is the mandatory
  blocked section.
- **No acceptance criteria** — tasks no one can call done, so "done" becomes a feeling. The
  cure is one observable criterion per task, written first.
- **Ignored risks** — a risk log written once and never reviewed. The cure is an owner per
  risk and a review every cadence.
- **Stale plans** — a plan that stopped matching reality two weeks ago. The cure is the fixed
  cadence and moving tasks on done, not on effort.
- **Untracked decisions** — choices made in chat and relitigated later. The cure is a linked
  decision note per material choice.

## Worked example: a new project, set up and reported

### Setting up the project record

A founder starts a project to ship a paid waitlist for a side product. The project note,
created via [second-brain-crud](../../../obsidian/second-brain-crud/SKILL.md):

```markdown
---
type: project
status: active
owner: "[[Lucas]]"
company: "[[Sideproject Inc]]"
cadence: weekly
created: 2026-06-22
---

# Paid waitlist launch

**Goal:** 100 paying waitlist signups by 2026-08-01.

**Scope**
- In: landing page, Stripe checkout, confirmation email.
- Out: full product, referral program, annual billing.

## Milestones
- [ ] 2026-07-04 — Landing page live (done: public URL renders, lighthouse > 90)
- [ ] 2026-07-18 — Checkout works (done: a real card completes a test purchase)
- [ ] 2026-08-01 — 100 paid signups (done: Stripe dashboard shows 100 paid)

## Critical path
Landing page → checkout → launch announcement. Email copy runs in parallel (slack).

## Tasks (current milestone)
- [ ] Build landing hero — accept: hero renders on mobile + desktop, CTA scrolls to form
- [ ] Wire signup form to store — accept: a submitted email appears in the table within 2s

## Risks
- Stripe approval delay — likelihood: med, impact: high, owner: [[Lucas]]
- Landing copy underperforms — likelihood: med, impact: med, owner: [[Lucas]]

## Decisions
- [[Decision - Stripe over Paddle]]
```

Note the shape: a testable goal, an explicit out-of-scope line, milestones with
done-conditions, a named critical path, tasks each carrying one acceptance criterion, owned
risks, and a linked decision note. WIP is held at two open tasks. The note links to the owner,
the company, and the decision — so a vault query on `[[Sideproject Inc]]` surfaces this project
beside everything else that client touches.

### The first weekly status update

```markdown
## Status — 2026-06-29

**Changed**
- Landing hero shipped; renders on mobile + desktop, CTA wired. (acceptance met)
- Signup form persists to the store in ~1s. (acceptance met)

**Next**
- Stand up Stripe checkout in test mode.
- Draft the confirmation email.

**Blocked**
- Stripe account still in review → traces to risk "Stripe approval delay". Submitted
  2026-06-24, SLA is 5 business days; checkout milestone slips if review runs past 2026-07-02.
```

The update is three parts, the blocker names the risk it traces to and the milestone it
threatens, and a reader learns in ten seconds what moved and what is at risk. Had Stripe been
fine, the blocked section would read "none blocked" rather than vanish.

## Completion checklist

A project record is in good standing when every line holds, or a failing line carries a dated,
owned exception:

- [ ] Goal states a testable outcome, not an activity.
- [ ] Scope names what is in and an explicit out-of-scope line.
- [ ] 3–7 milestones, each dated with a done-condition.
- [ ] Near-term tasks each carry one observable acceptance criterion.
- [ ] The critical path is named.
- [ ] Open tasks sit at or below the WIP limit.
- [ ] The latest cadence entry carries the current date.
- [ ] Every open risk has an owner.
- [ ] Every material decision links to a decision note.
- [ ] The status update names changed, next, and blocked.
- [ ] The project links to its owner and at least one company-or-commitment note, and the
      links resolve.
